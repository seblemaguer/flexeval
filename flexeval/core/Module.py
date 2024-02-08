# coding: utf8
# license : CeCILL-C

import logging

import abc

import json

from flask import Blueprint, current_app, abort
from flask import render_template as flask_render_template

from flexeval.core import ProviderFactory
from .Config import Config
from flexeval.core.providers.auth import AuthProvider, UserModel, VirtualAuthProvider

from flexeval.utils import make_global_url, make_absolute_path
from flexeval.database import Model


class ModuleError(Exception):
    """Default exception for Module errors

    Attributes
    ----------
    message: string
        The error message
    """

    def __init__(self, message):
        self.message = message


class MalformationError(ModuleError):
    """Exception raised when something is malformed"""

    pass


class MalformationTemplateError(MalformationError):
    """Exception raised when a template is malformed

    Attributes
    ==========
    file: string or File
       The template file
    """

    def __init__(self, tpl_file):
        super().__init__('The template "%s" is malformed' % tpl_file)
        self.file = tpl_file


class NotAnAuthProvider(ModuleError):
    """Exception raised when the provider given is not an AuthProvider"""

    pass


class NotAUserModel(ModuleError):
    """Exception raised when an object is not instanciating the UserModel class"""

    pass


class OverwritingClassAttributesForbidden(ModuleError):
    """Exception raised when an object is not instanciating the UserModel class"""

    pass


class UserModelAttributesMeta(type(Model)):
    def __setattr__(self, name, val):
        if hasattr(self, "__lock__"):
            if self.__lock__ and not (name == "__lock__"):
                if hasattr(self, name):
                    raise OverwritingClassAttributesForbidden("Class Attributes:" + name + " already existing.")

        super().__setattr__(name, val)


class Module(Blueprint, abc.ABC):
    default_checker_handlers = dict()

    def __init__(self, namespace, subname=None):
        # Define logger
        self.logger = logging.getLogger(f"{self.__class__.__name__} ({namespace}:{subname})")

        self.namespace = namespace.split(".")
        self.subname = subname
        self.mod_rep = self.namespace[2]
        self.checker_handlers = dict()

        super().__init__(self.__class__.name_type + ":" + self.get_mod_name(), namespace)

        if not (ProviderFactory().exists("auth_mod_" + self.__class__.name_type)):
            self.__class__.set_authProvider(VirtualAuthProvider)

    @property
    def authProvider(self):
        return self.__class__.get_authProvider()

    @classmethod
    def connect_default_checker_handler(cls, name, handler):
        cls.default_checker_handlers[name] = handler

    def connect_checker_handler(self, name, handler):
        self.checker_handlers[name] = handler

    @classmethod
    def disconnect_default_checker_handler(cls, name):
        cls.default_checker_handlers.pop(name, None)

    def disconnect_checker_handler(self, name):
        self.checker_handlers.pop(name, None)

    @classmethod
    def get_authProvider(cls):
        if not (ProviderFactory().exists("auth_mod_" + cls.name_type)):
            cls.set_authProvider(VirtualAuthProvider)

        return ProviderFactory().get("auth_mod_" + cls.name_type)

    @classmethod
    def set_authProvider(cls, cls_auth):
        cls.init_UserModel(cls_auth)

        if not (
            isinstance(
                cls_auth("auth_mod_" + cls.name_type, cls.homepage, cls.userModel),
                AuthProvider,
            )
        ):
            raise NotAnAuthProvider(str(cls_auth) + " is not an AuthProvider sub-class")

    @classmethod
    def init_UserModel(cls, cls_auth):
        __userBase__ = cls_auth.__userBase__
        table_name = cls.__name__ + "User"
        table_type = cls.name_type + "User"

        if not (hasattr(cls, "userModel")):
            cls.userModel = UserModelAttributesMeta(
                table_type,
                (
                    UserModel,
                    Model,
                ),
                {"__abstract__": True, "__tablename__": table_name},
            )
            setattr(cls.userModel, "__lock__", True)

        if __userBase__ is not None:
            bases = __userBase__.__bases__
            try:
                assert len(bases) == 1
                assert UserModel in bases
            except Exception as e:
                raise NotAUserModel(__userBase__ + " is not only or not a subClass of UserModel")

            if hasattr(cls, "userModel_init"):
                if __userBase__ in list(cls.userModel.__bases__):
                    pass
                else:
                    raise MalformationError("Two differents auth provider defined for " + cls.__name__ + ".")
            else:
                cls.userModel.__lock__ = False
                cls.userModel = UserModelAttributesMeta(
                    table_type,
                    (cls.userModel, __userBase__),
                    {"__abstract__": False, "__tablename__": table_name},
                )
                setattr(cls.userModel, "__lock__", True)
                cls.userModel_init = True

    @abc.abstractmethod
    def url_for(self, endpoint, **kwargs):
        pass

    @classmethod
    def get_UserModel(cls):
        return cls.get_authProvider().userModel

    def __enter__(self):
        self.logger.info("Registering module: %s" % self.mod_rep)
        ProviderFactory().get("templates").register(self.mod_rep)
        return self

    def __exit__(self, *args):
        try:
            current_app.register_blueprint(self, url_prefix=self.local_rule())
            self.logger.info("%s is loaded and bound to: %s" % (self.get_mod_name(), self.local_rule()))
        except Exception as e:
            raise MalformationError(
                "There are already a " + self.__class__.__name__ + " module named: " + self.get_mod_name()
            )

    def local_rule(self):
        return "/" + self.__class__.name_type + "/" + self.get_mod_name()

    def get_mod_name(self):
        if self.subname is None:
            return self.mod_rep
        else:
            return self.mod_rep + ":" + self.subname

    def valid_connection_required(self, f):
        def wrapper(*args, **kwargs):
            (user_validates, condition) = self.authProvider.validates_connection()

            if not user_validates:
                if (condition is None) or (condition == "connected"):
                    abort(401)
                elif condition in self.checker_handlers:
                    return self.checker_handlers[condition](self)  # TODO: Arguments
                elif condition in self.__class__.default_checker_handlers:
                    return self.__class__.default_checker_handlers[condition](self)  # TODO: Arguments
                else:
                    raise Exception('No handler to deal with invalid condition "%s"' % condition)

            return f(*args, **kwargs)

        return wrapper

    @classmethod
    def render_template(cls, path_template, args={}, variables={}, parameters={}):
        """Class method which renders the given template

        Parameters
        ----------
        self: Module
            The current Module object
        path_template: string or file
            The path to the template
        args: dict of strings
            The dictionnary of arguments
        variables: dict of strings
            The dictionnary of variables
        parameters: dict of strings
            The dictionnary of parameters

        Returns
        -------
        string: the rendered template
        """

        try:
            args["auth"] = ProviderFactory().get("auth_mod_" + cls.name_type)
            args["homepage"] = make_global_url(cls.homepage)
        except Exception as e:
            args["auth"] = VirtualAuthProvider()
            args["homepage"] = make_global_url("/")

        args["module_class"] = cls.__name__

        variables.update(Config().data()["variables"])

        def read_file(filename):
            with open(make_absolute_path(filename)) as f:
                return f.read()

        def read_json(filename):
            with open(make_absolute_path(filename)) as f:
                return json.load(f)

        def get_variable(key, *args, **kwargs):
            if "default_value" in kwargs:
                default_value = kwargs["default_value"]
            else:
                default_value = None

            if key in parameters:
                try:
                    try:
                        return parameters[key](*args, **kwargs)
                    except Exception as e:
                        del kwargs["default_value"]
                        return parameters[key](*args, **kwargs)
                except Exception as e:
                    return parameters[key]
            else:
                if key in variables:
                    return variables[key]
                else:
                    return default_value

        def get_asset(name, rep=None):
            return make_global_url(ProviderFactory().get("assets").local_url(name, rep))

        args["read_file"] = read_file
        args["read_json"] = read_json
        args["get_variable"] = get_variable
        args["get_asset"] = get_asset
        args["get_template"] = ProviderFactory().get("templates").get
        args["make_url"] = make_global_url

        try:
            return flask_render_template(path_template, **args)
        except Exception as e:
            raise MalformationTemplateError(path_template)
