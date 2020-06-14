# coding: utf8
# license : CeCILL-C

from contextlib import contextmanager
import sqlalchemy

from flask import Blueprint, current_app, abort
from flask import render_template as flask_render_template

from .Provider import Provider
from .Config import Config
from .AuthProvider import AuthProvider, UserBase

from flexeval.utils import safe_copy_rep, make_global_url, redirect
from flexeval.core.providers.auth import virtual
from flexeval.database import Model

class ModuleError(Exception):
    pass

class MalformationError(ModuleError):

    def __init__(self,message):
        self.message = message

class MalformationTemplateError(MalformationError):

    def __init__(self,file):
        self.file = file

class NotAnAuthProvider(ModuleError):

    def __init__(self,message):
        self.message = message

class NotAUserBase(ModuleError):

    def __init__(self,message):
        self.message = message

class OverwritingClassAttributesForbidden(ModuleError):

    def __init__(self,message):
        self.message = message

class UserModelAttributesMeta(type(Model)):
    def __setattr__(self,name,val):
        if hasattr(self,"__lock__"):
            if self.__lock__ and not(name == "__lock__"):
                if hasattr(self,name):
                    raise OverwritingClassAttributesForbidden("Class Attributes:"+name+" already existing.")

        super().__setattr__(name,val)

class Module(Blueprint):

    def __init__(self,namespace,subname=None):
        self.namespace = namespace.split(".")
        self.subname = subname
        self.mod_rep = self.namespace[2]

        super().__init__(self.__class__.name_type+":"+self.get_mod_name(),namespace)

        if not(Provider().exists("auth_mod_"+self.__class__.name_type)):
            self.__class__.set_authProvider(virtual)

    @classmethod
    def get_authProvider(cls):
        if not(Provider().exists("auth_mod_"+cls.name_type)):
            cls.set_authProvider(virtual)

        return Provider().get("auth_mod_"+cls.name_type)

    @property
    def authProvider(self):
        return self.__class__.get_authProvider()

    @classmethod
    def set_authProvider(cls,cls_auth):

        cls.init_UserModel(cls_auth)

        if not(isinstance(cls_auth("auth_mod_"+cls.name_type, cls.homepage,cls.userModel),AuthProvider)):
            raise NotAnAuthProvider(str(cls_auth)+" is not an AuthProvider sub-class")

    @classmethod
    def init_UserModel(cls,cls_auth):

        __userBase__ = cls_auth.__userBase__

        if not(hasattr(cls,"userModel")):
            cls.userModel = UserModelAttributesMeta(cls.name_type+"User",(UserBase,Model,),{"__abstract__":True,"__tablename__":cls.__name__+"_User"})
            setattr(cls.userModel,"__lock__",True)

        if __userBase__ is not None:

            bases = __userBase__.__bases__

            try:
                assert len(bases) == 1
                assert UserBase in bases
            except Exception as e:
                raise NotAUserBase(__userBase__+" is not only or not a subClass of UserBase")

            if hasattr(cls,"userModel_init"):
                if __userBase__ in list(cls.userModel.__bases__):
                    pass
                else:
                    raise MalformationError("Two differents auth provider defined for "+cls.__name__+".")
            else:

                cls.userModel.__lock__ = False
                cls.userModel = UserModelAttributesMeta(cls.name_type+"User",(cls.userModel,__userBase__),{"__abstract__":False,"__tablename__":cls.__name__+"_User"})
                setattr(cls.userModel,"__lock__",True)
                cls.userModel_init = True

    def url_for(self,endpoint,**kwargs):
        raise NotImplementedError()

    @classmethod
    def get_UserModel(cls):
        return cls.get_authProvider().userModel

    def __enter__(self):

        Provider().get("templates").register(self.mod_rep)

        return self

    def __exit__(self, *args):

        try:
            current_app.register_blueprint(self,url_prefix=self.local_rule())
            print(" * "+self.__class__.__name__+" named "+self.get_mod_name()+" is loaded and bound to: "+self.local_rule())
        except Exception as e:
            raise MalformationError("There are already a "+self.__class__.__name__+" module named: "+self.get_mod_name())

    def local_rule(self):
        return "/"+self.__class__.name_type+'/'+self.get_mod_name()

    def get_mod_name(self):
        if self.subname is None:
            return self.mod_rep
        else:
            return self.mod_rep+":"+self.subname

    def connection_required(self,f):
        def wrapper(*args,**kwargs):

            if not(self.authProvider.is_connected):
                abort(401)

            return f(*args,**kwargs)
        return wrapper

    @classmethod
    def render_template(cls,path_template,args={},variables={},parameters={}):

        try:
            args["auth"] = Provider().get("auth_mod_"+cls.name_type)
            args["homepage"] = make_global_url(cls.homepage)
        except Exception as e:
            args["auth"] = virtual()
            args["homepage"] = make_global_url('/')

        args["module_class"] = cls.__name__

        variables.update(Config().data()["variables"])
        def get_variable(key,*args,**kwargs):

            if "default_value" in kwargs:
                default_value=kwargs["default_value"]
            else:
                default_value = None

            if key in parameters:
                try:
                    try:
                        return parameters[key](*args,**kwargs)
                    except Exception as e:
                        del kwargs["default_value"]
                        return parameters[key](*args,**kwargs)
                except Exception as e:
                    return parameters[key]
            else:
                if key in variables:
                    return variables[key]
                else:
                    return default_value

        def get_asset(name,rep=None):
            return make_global_url(Provider().get("assets").local_url(name,rep))

        args["get_variable"] = get_variable
        args["get_asset"] = get_asset
        args["get_template"] = Provider().get("templates").get
        args["make_url"] = make_global_url

        try:
            return flask_render_template(path_template,**args)
        except Exception as e:
            raise MalformationTemplateError(path_template)
