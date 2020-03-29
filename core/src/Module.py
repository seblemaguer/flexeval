import os

from flask import Blueprint,request,session, abort
from core.utils import reserved_name, app,safe_copy_rep,NAME_REP_CONFIG,ROOT,get_provider, admin_mod, config

class Module(Blueprint):

    def __init__(self,modname,name,**args):
        Blueprint.__init__(self,modname,name,**args)
        self.name = name

        splitname = self.name.split(".")
        self.rep_mod_name =  "/".join(i for i in splitname)
        self.mod_name = splitname[len(splitname)-1]
        previous_rep = splitname[len(splitname)-2]

        if not(os.path.isdir(ROOT+"/"+self.rep_mod_name)):

            self.rep_mod_name = ""
            self.rep_mod_name =  "/".join(i for i in splitname[:len(splitname) - 1])
            self.mod_name = splitname[len(splitname)-2]
            previous_rep = splitname[len(splitname)-3]

            if not(os.path.isdir(ROOT+"/"+self.rep_mod_name)):
                raise Exception("MISTAKE 42: A file in a file ? ")

        if(self.mod_name in reserved_name):
            raise Exception("You can't name a module "+self.mod_name)

        if not(previous_rep == "mods"):
            raise Exception("Module need to be define at the root of your module (/core/mods/my_module/MonSuperModule.py). ")

    def __enter__(self):
        safe_copy_rep(ROOT+"/"+self.rep_mod_name+"/templates",NAME_REP_CONFIG+"/.tmp/templates/"+self.mod_name)
        return self

    def __exit__(self, *args):
        app.register_blueprint(self,url_prefix='/'+self.mod_name) # Register Blueprint


class AdminModule(Module):

    def __init__(self,modname,name,title,description,**args):
        Module.__init__(self,modname,name,**args)

        admin_mod.append(self)

        self.TITLE = title
        self.DESCRIPTION = description

        self.before_request(AdminModule.authentification)

    @classmethod
    def authentification(cls):
        if "admin_password" in request.form:
            session["admin_password"] = request.form["admin_password"]

        if "admin_password" in session:
            if not(session["admin_password"] == config["admin"]["password"]):
                abort(401)
        else:
            abort(401)

    def __exit__(self, *args):
        app.register_blueprint(self,url_prefix='/admin/'+self.mod_name)


class StageModule(Module):

    def __init__(self,modname,name,requiere_auth=True,**args):
        Module.__init__(self,modname,name,**args)

        if requiere_auth:
            self.before_request(StageModule.check_auth)

    @classmethod
    def check_auth(cls):
        get_provider("auth").get()

    def requiere_auth(func):
        def requiere_auth_and_call(*args, **kwargs):
            StageModule.check_auth()

            return func(*args, **kwargs)
        return requiere_auth_and_call
