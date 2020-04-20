import os
import shutil
import json
import importlib

from flask import current_app, request

from perceval.utils import safe_copy_rep,AppSingleton, redirect

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

class Config(metaclass=AppSingleton):

    def __init__(self):

        self.config = None
        self.modules = []

        self.load_file()
        self.stages()
        self.default_authProvider_for_StageModule()

        self.admin_mods()

        current_app.add_url_rule('/','entrypoint',self.entrypoint)
        current_app.add_url_rule('/admin/','entrypoint_admin',self.entrypoint_admin)

        print(" * WebService configuration made; using "+current_app.config["PERCEVAL_INSTANCE_DIR"]+"/structure.json.")

    def data(self):
        return self.config

    def admin_mods(self):
        if "mods" in self.data()["admin"]:
            for mods in self.data()["admin"]["mods"]:
                try:
                    self.load_module(mods["mod"])
                except Exception as e:
                    raise MalformationError("Issue in structure.json for "+str(mods))

    def entrypoint_admin(self):
        from .Admin import AdminModule
        args_GET ="?"
        for args_key in request.args.keys():
            args_GET = args_GET + args_key + "=" + request.args[args_key] + "&"

        try:
            return redirect(AdminModule.get_local_url_for(self.data()["admin"]["entrypoint"])+args_GET)
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
            with open(current_app.config["PERCEVAL_INSTANCE_DIR"]+'/structure.json') as config:
                self.config = json.load(config)
        except Exception as e:
            raise ConfigError("Issue when loading structure.json.",current_app.config["PERCEVAL_INSTANCE_DIR"]+'/structure.json')

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

        while not(next_stage is None):

            current = next_stage
            current_stage_name = next_stage_name

            try:
                assert current_stage_name.replace("_","").isalpha()
            except Exception as e:
                raise MalformationError("Stage name:"+current_stage_name+" is incorrect. Only alphabet's and '_' symbol caracteres are allow. ")

            # Activate module (attr type)
            try:
                module_name = current["type"]
            except Exception as e:
                raise MalformationError("Field: type is missing from the stage: "+current_stage_name)

            self.load_module(module_name)

            # Next stage ?
            if "next" in current:
                next_stage_name = current["next"]
                if next_stage_name in self.config["stages"]:
                    next_stage = self.config["stages"][current["next"]]
                else:
                    raise NextStageNotFoundError(current_stage_name,next_stage_name)
            else:
                next_stage = None

    def load_module(self,name):
        name = name.split(":")
        name = name[0]

        if(name not in self.modules):

            try:
                lib_imported = importlib.import_module("perceval.mods."+name)
                self.modules.append(name)
            except Exception as e:
                raise LoadModuleError("Module: "+name+" doesn't exist or can't be initialized properly.")

    def default_authProvider_for_StageModule(self):
        from .Stage import StageModule
        from perceval.core.providers.auth import virtual,anon

        if isinstance(StageModule.get_authProvider(),virtual):
            StageModule.set_authProvider(anon)
