# coding: utf8
# license : CeCILL-C

# Global/Systems
from typing import Any
import pathlib
import logging
from collections import deque

# Yaml
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, configuration_file: pathlib.Path):
        super().__init__()

        # Define logger
        self._logger = logging.getLogger(self.__class__.__name__)

        self._data: dict[str, Any] = dict()
        self.load_file(configuration_file)

        self._logger.info(f"WebService configuration made using {configuration_file}")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def list_modules(self) -> list[str]:

        # No specific modules to instanciate
        if "mods" not in self._data:
            return []

        list_modules: list[str] = []
        for mods in self._data["mods"]:
            list_modules.append(mods["mod"])
        return list_modules

    def list_admin_modules(self) -> list[str]:

        # No specific modules to instanciate
        if ("admin" not in self._data) or ("mods" not in self._data["admin"]):
            return []

        list_modules: list[str] = []
        for cur_mod in self._data["admin"]["mods"].keys():
            list_modules.append(cur_mod)

        return list_modules

    def get_admin_entrypoint(self) -> str:
        return self._data["admin"]["entrypoint"]

    def list_reachable_stages(self, start: str = "") -> list[str]:

        if not start:
            start = self._data["entrypoint"]

        next_stages: deque[str] = deque()
        next_stages.append(start)

        list_stages: list[str] = list()
        while next_stages:
            # Retrieve current stage information
            current_stage_name: str = next_stages.popleft()
            current_stage: dict[str, Any] = self._data["stages"][current_stage_name]
            list_stages.append(current_stage_name)

            #
            if "next" in current_stage:
                if isinstance(current_stage["next"], list):
                    for next_stage in current_stage["next"]:
                        if next_stage not in next_stages:
                            next_stages.append(next_stage)
                elif isinstance(current_stage["next"], str):
                    if current_stage["next"] not in next_stages:
                        next_stages.append(current_stage["next"])
                else:
                    type_next = type(current_stage["next"])
                    raise ConfigError(
                        f"The next stage field only accepts a list of names or one name, not a {type_next}"
                    )
        return list_stages

    def get_entrypoint(self) -> str:
        return self._data["entrypoint"]

    def load_file(self, configuration_file: pathlib.Path):
        try:
            with open(configuration_file, encoding="utf-8") as config_stream:
                self._data = load(config_stream, Loader=Loader)
        except Exception:
            raise ConfigError(f"Issue when loading {configuration_file}.", configuration_file)

    def get_module_config(self, module_name: str) -> dict[str, Any]:
        config: dict[str, Any] = dict()
        config["variables"] = self._data["variables"]
        if ("mods" in self._data) and (module_name in self._data["mods"]):
            for k, v in self._data["mods"][module_name].items():
                config[k] = v
        return config

    def get_admin_config(self, module_name: str) -> dict[str, Any]:
        module_name = module_name.replace("flexeval.mods.", "")
        return self._data["admin"]["mods"][module_name]

    def get_stage_config(self, stage_name: str) -> dict[str, Any]:
        config: dict[str, Any] = self._data["stages"][stage_name]
        if ("next" in config.keys()) and (isinstance(config["next"], str)):
            config["next"] = [config["next"]]
        return config

    def get_stage_configs(self, stage_names: list[str]) -> dict[str, Any]:
        configs: dict[str, Any] = dict()
        for stage_name in stage_names:
            configs[stage_name] = self.get_stage_config(stage_name)

        return configs
