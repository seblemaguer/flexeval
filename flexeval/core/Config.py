# coding: utf8
# license : CeCILL-C

# Global/Systems
import os
import importlib
import logging

# Yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Flask
from flask import current_app, request

# Utils
from flexeval.core import ProviderFactory
from flexeval.utils import AppSingleton, redirect


STRUCTURE_CONFIGURATION_BASENAME = "structure"


class ConfigError(Exception):
    pass


class MalformationError(ConfigError):
    def __init__(self, message):
        self.message = message


class NextStageNotFoundError(ConfigError):
    def __init__(self, stage, next_stage):
        self.stage = stage
        self.next_stage = next_stage
        self.message = (
            "The next stage after "
            + self.stage
            + ", named "
            + self.next_stage
            + " can't be found in "
            + STRUCTURE_CONFIGURATION_BASENAME
        )


class LoadModuleError(ConfigError):
    def __init__(self, message):
        self.message = message


class Config(metaclass=AppSingleton):
    def __init__(self):
        # Define logger
        self._logger = logging.getLogger(self.__class__.__name__)

        self.config = None
        self.modules = []
        self.admin_modules = []
        self._stages = dict()

        self.load_file()

        # Register and load modules
        self.setup_mods()
        self.setup_admin_mods()

        # Load stages
        self.stages()

        # Define provider
        self.default_authProvider_for_StageModule()

        # Finalize templating
        ProviderFactory().get("templates").register_instance()

        current_app.add_url_rule("/", "entrypoint", self.entrypoint)
        current_app.add_url_rule("/admin/", "entrypoint_admin", self.entrypoint_admin)

        self._logger.info(
            "WebService configuration made; using "
            + os.path.join(current_app.config["FLEXEVAL_INSTANCE_DIR"], "%s.yaml." % STRUCTURE_CONFIGURATION_BASENAME)
        )

    def get_stages(self, module_name):
        return self._stages[module_name]

    def data(self):
        return self.config

    def setup_mods(self):
        if "mods" in self.data():
            for mods in self.data()["mods"]:
                try:
                    self.load_module(mods["mod"])
                except Exception as e:
                    raise MalformationError("Issue in structure.json for " + str(mods))
        else:
            self.data()["mods"] = []

    def setup_admin_mods(self):
        if "admin" in self.data():
            if "mods" in self.data()["admin"]:
                for mods in self.data()["admin"]["mods"]:
                    self.admin_modules.append(mods)
                    try:
                        self.load_module(mods["mod"])
                    except Exception as e:
                        raise MalformationError("Issue in structure.json for " + str(mods))
            else:
                self.data()["admin"]["mods"] = []

            entrypoint_admin_mod = self.data()["admin"]["entrypoint"]
            self.data()["admin"]["mods"].append(entrypoint_admin_mod)

            try:
                self.load_module(entrypoint_admin_mod["mod"])
            except Exception as e:
                raise MalformationError("Issue in " + STRUCTURE_CONFIGURATION_BASENAME + ".yaml for " + str(mods))

    def entrypoint_admin(self):
        from .Admin import AdminModule

        args_GET = "?"
        for args_key in request.args.keys():
            args_GET = args_GET + args_key + "=" + request.args[args_key] + "&"

        try:
            return redirect(AdminModule.get_local_url_for(self.data()["admin"]["entrypoint"]["mod"]) + args_GET)
        except Exception as e:
            raise MalformationError("No entrypoint for admin set-up.")

    def entrypoint(self):
        from .Stage import Stage

        args_GET = "?"
        for args_key in request.args.keys():
            args_GET = args_GET + args_key + "=" + request.args[args_key] + "&"

        return redirect(Stage(self.data()["entrypoint"]).local_url + args_GET)

    def load_file(self):
        try:
            with open(
                os.path.join(
                    current_app.config["FLEXEVAL_INSTANCE_DIR"],
                    "%s.yaml" % STRUCTURE_CONFIGURATION_BASENAME,
                ),
                encoding="utf-8",
            ) as config_stream:
                self.config = load(config_stream, Loader=Loader)
        except Exception as e:
            raise ConfigError(
                "Issue when loading structure.json.",
                os.path.join(
                    current_app.config["FLEXEVAL_INSTANCE_DIR"],
                    "%s.yaml" % STRUCTURE_CONFIGURATION_BASENAME,
                ),
            )

    def load_stage(self, current_stage_name):
        current_stage = self.config["stages"][current_stage_name]

        try:
            assert current_stage_name.replace("_", "").isalnum()
        except Exception as e:
            raise MalformationError(
                "Stage name:"
                + current_stage_name
                + " is incorrect. Only alphabet's and '_' symbol caracteres are allow. "
            )

        # Activate module (attr type)
        try:
            module_name = current_stage["type"]
        except Exception as e:
            raise MalformationError("Field: type is missing from the stage: " + current_stage_name)

        self.load_module(module_name)

        # Save Stage
        if module_name not in self._stages:
            self._stages[module_name] = list()
        self._stages[module_name].append(current_stage_name)

        # Next stage ?
        if "next" in current_stage:
            if isinstance(current_stage["next"], dict):
                next_stage_names = current_stage["next"].values()
            else:
                next_stage_names = [current_stage["next"]]

            for next_stage_name in next_stage_names:
                if next_stage_name in self.config["stages"]:
                    next_stage = self.config["stages"][next_stage_name]
                    self.load_stage(next_stage_name)
                else:
                    raise NextStageNotFoundError(current_stage_name, next_stage_name)

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
            raise NextStageNotFoundError("entrypoint", self.config["entrypoint"])

        self.load_stage(next_stage_name)

    def load_module(self, name):
        name = name.split(":")
        name = name[0]

        self._logger.info('Loading moodule "%s"' % name)

        if name not in self.modules:
            try:
                lib_imported = importlib.import_module("flexeval.mods." + name)
                self.modules.append(name)
            except Exception as e:
                raise LoadModuleError("Module: " + name + " doesn't exist or can't be initialized properly.")

    def default_authProvider_for_StageModule(self):
        from .Stage import StageModule
        from flexeval.core.providers.auth import VirtualAuthProvider, AnonAuthProvider

        if isinstance(StageModule.get_authProvider(), VirtualAuthProvider):
            StageModule.set_authProvider(AnonAuthProvider)
