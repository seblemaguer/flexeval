# coding: utf8
# license : CeCILL-C

import os
import shutil
import json
import importlib

from flask import current_app, request

from flexeval.utils import safe_copy_rep,AppSingleton, redirect

class ConfigError(Exception):
    pass

class ConfigFileError(ConfigError):

    def __init__(self, message, file):
        self.message = message
        self.file = file

class MalformationError(ConfigError):

    def __init__(self,message):
        self.message = message

class NextStageNotFoundError(ConfigError):

    def __init__(self, stage, next_stage):
        self.stage = stage
        self.next_stage = next_stage
        self.message = "The next stage after "+self.stage+", named "+self.next_stage+" can't be found in structure.json."

class LoadModuleError(ConfigError):

    def __init__(self,message):
        self.message = message

class GdprComplianceError(ConfigError):
    def __init__(self,message):
        self.message = message

class Config(metaclass=AppSingleton):

    def __init__(self):

        self.config = None
        self.modules = []
        self.admin_modules = []

        self.load_file()
        self.stages()
        self.default_authProvider_for_StageModule()

        self.setup_admin_mods()

        self.legal_terms()

        try:
            assert("gdpr_compliance" in self.config)
        except Exception as e:
            raise GdprComplianceError("Defined a level of GDPR Compliance (field gdpr_compliance) required for this website: strict or relax. The field need to be defined in the following file: "+current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/structure.json.")

        if(self.config["gdpr_compliance"] == "strict"):
            from .LegalTerms import LegalTerms
            try:
                assert(LegalTerms().is_GDPR_Compliant())
            except Exception as e:
                raise GdprComplianceError("This website require to be fully GDPR Compliant to be run.")

        elif(self.config["gdpr_compliance"] == "relax"):
            pass
        else:
            raise GdprComplianceError("The level of GDPR Compliance (field gdpr_compliance) need to be one of these two values: strict or relax")


        current_app.add_url_rule('/','entrypoint',self.entrypoint)
        current_app.add_url_rule('/admin/','entrypoint_admin',self.entrypoint_admin)

        print(" * WebService configuration made; using "+current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/structure.json.")

    def data(self):
        return self.config

    def legal_terms(self):
        from .LegalTerms import LegalTerms
        LegalTerms()

    def setup_admin_mods(self):
        if "admin" in self.data():
            if "mods" in self.data()["admin"]:
                for mods in self.data()["admin"]["mods"]:
                    self.admin_modules.append(mods)
                    try:
                        self.load_module(mods["mod"])
                    except Exception as e:
                        raise MalformationError("Issue in structure.json for "+str(mods))
            else:
                self.data()["admin"]["mods"] = []

            entrypoint_admin_mod = self.data()["admin"]["entrypoint"]
            self.data()["admin"]["mods"].append(entrypoint_admin_mod)

            try:
                self.load_module(entrypoint_admin_mod["mod"])
            except Exception as e:
                raise MalformationError("Issue in structure.json for "+str(mods))

    def entrypoint_admin(self):
        from .Admin import AdminModule

        args_GET ="?"
        for args_key in request.args.keys():
            args_GET = args_GET + args_key + "=" + request.args[args_key] + "&"

        try:
            return redirect(AdminModule.get_local_url_for(self.data()["admin"]["entrypoint"]["mod"])+args_GET)
        except Exception as e:
            raise MalformationError("No entrypoint for admin set-up.")

    def entrypoint(self):
        from .Stage import Stage

        args_GET ="?"
        for args_key in request.args.keys():
            args_GET = args_GET + args_key + "=" + request.args[args_key] + "&"

        return redirect(Stage(self.data()["entrypoint"]).local_url+args_GET)

    def load_file(self):
        try:
            with open(current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/structure.json',encoding='utf-8') as config:
                self.config = json.load(config)
        except Exception as e:
            raise ConfigError("Issue when loading structure.json.",current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/structure.json')

    def load_stage(self,current_stage_name):

        current_stage = self.config["stages"][current_stage_name]

        try:
            assert current_stage_name.replace("_","").isalpha()
        except Exception as e:
            raise MalformationError("Stage name:"+current_stage_name+" is incorrect. Only alphabet's and '_' symbol caracteres are allow. ")

        # Activate module (attr type)
        try:
            module_name = current_stage["type"]
        except Exception as e:
            raise MalformationError("Field: type is missing from the stage: "+current_stage_name)

        self.load_module(module_name)

        # Next stage ?
        if "next" in current_stage:
            if isinstance(current_stage["next"],dict):
                next_stage_names = current_stage["next"].values()
            else:
                next_stage_names = [current_stage["next"]]

            for next_stage_name in next_stage_names:
                if next_stage_name in self.config["stages"]:
                    next_stage = self.config["stages"][next_stage_name]
                    self.load_stage(next_stage_name)
                else:
                    raise NextStageNotFoundError(current_stage_name,next_stage_name)

    def stages(self):

        try:
            assert "entrypoint" in self.config
            assert "stages" in self.config
        except Exception as e:
            raise MalformationError("Field: entrypoint or/and stages are missing. ")

        try:
            current_stage_name = "entrypoint"
            next_stage_name = self.config[current_stage_name]
            next_stage = self.config["stages"][next_stage_name]
        except Exception as e:
            raise NextStageNotFoundError("entrypoint",self.config["entrypoint"])

        self.load_stage(next_stage_name)

    def load_module(self,name):
        name = name.split(":")
        name = name[0]

        if(name not in self.modules):

            try:
                lib_imported = importlib.import_module("flexeval.mods."+name)
                self.modules.append(name)
            except Exception as e:
                raise LoadModuleError("Module: "+name+" doesn't exist or can't be initialized properly.")

    def default_authProvider_for_StageModule(self):
        from .Stage import StageModule
        from flexeval.core.providers.auth import virtual,anon

        if isinstance(StageModule.get_authProvider(),virtual):
            StageModule.set_authProvider(anon)
