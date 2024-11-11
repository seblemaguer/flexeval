# python
from typing import Any
import logging
from logging import Logger
import importlib


from werkzeug import Response
from flask import request, current_app

from flexeval.utils import redirect

# Flexeval core imports
from .providers import provider_factory
from .providers.content import TemplateProvider
from .config import Config
from .admin import AdminModule
from .stage import StageModule, StageGraph
from .providers.auth import VirtualAuthProvider, AnonAuthProvider


class CampaignInstanceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class LoadModuleError(CampaignInstanceError):
    def __init__(self, message: str):
        super().__init__(message)


class CampaignInstance:
    """Entry point of the campaign instance

    This class deals with all the instantiations necessary for the evaluation campaign to be functionnal.
    This implies:
      - loading the modules, admin modules and stages
      - registering the different rules and providers

    To do so, a configuration object is necessary
    """

    def __init__(
        self,
        config: Config | None = None,
    ):
        """Initialisation method

        Just initialise the different fields. If a configuration
        object is provided, it also load all the components necessary
        for the campaign to run

        Parameters
        ----------
        config : Config| None
            The optional configuration object
        """
        # Define logger
        self._logger: Logger = logging.getLogger(self.__class__.__name__)
        self._config: Config | None = config
        self._modules: set[str] = set()
        self._stage_graph: StageGraph | None = None

        # The admin modules do not require a complicated setup, let' just deal with them in
        self._admin_entrypoint: str = ""
        self._admin_modules: dict[str, AdminModule] = dict()

        if config is not None:
            self.load_config(config)

    def load_config(self, config: Config):
        """Load the configuration and setup the campaign instance

        Parameters
        ----------
        config : Config
            The new configuration to be loaded
        """
        self._config = config

        self._load_modules()
        self._load_admin_modules()
        self._load_stages()

        # Register the providers some important information
        provider_factory.get(TemplateProvider.NAME).register_instance()  # type: ignore
        if isinstance(StageModule.get_auth_provider(), VirtualAuthProvider):
            StageModule.set_auth_provider(AnonAuthProvider)

        # Register the instance entry points
        current_app.add_url_rule("/", "entrypoint", self.goto_entrypoint)
        current_app.add_url_rule("/admin/", "entrypoint_admin", self.goto_admin_entrypoint)

    def _load_modules(self):
        """Load the modules and fill the list of available modules"""
        assert self._config is not None

        modules_to_load: list[str] = self._config.list_modules()
        for cur_module in modules_to_load:
            self._instanciate_module(cur_module)

    def _load_admin_modules(self):
        """Load the admin modules and fill the list of available admin modules

        This helper also prepare the admin entry point
        """
        assert self._config is not None

        # Load admin modules
        modules_to_load: list[str] = self._config.list_admin_modules()
        for cur_module in modules_to_load:
            self._instanciate_module(cur_module)

        # Load the entry point module
        self._admin_entrypoint = self._config.get_admin_entrypoint()
        self._instanciate_module(self._admin_entrypoint)

    def _load_stages(self):
        """Load the different stages (modules) of the campaigns

        This helper also prepare the campaign entry point
        """
        assert self._config is not None

        # Define the graph
        stages: list[str] = self._config.list_reachable_stages()
        stage_configs = self._config.get_stage_configs(stages)
        self._stage_graph = StageGraph(self._config.get_entrypoint(), stages, stage_configs)
        for cur_stage in self._stage_graph.list_stages().values():
            self._instanciate_module(cur_stage.mod_rep)

    def _instanciate_module(self, name_type: str):
        """Instanciate a module and add it to the list of available modules

        Parameters
        ----------
        name_type : str
            The name of the type of the module

        Raises
        ------
        LoadModuleError
            if the module can't be loaded
        """

        name_elts = name_type.split(":")
        name_type = name_elts[0]

        # The name is module is already loaded
        if name_type in self._modules:
            return

        self._logger.info(f'Loading module "{name_type}"')

        try:
            _ = importlib.import_module(f"flexeval.mods.{name_type}")
            self._modules.add(name_type)
        except Exception as ex:
            raise LoadModuleError(f"Module: {name_type} doesn't exist or can't be initialized properly.: {ex}")

    def goto_entrypoint(self) -> Response:
        """Generate the HTTP response to go to the entry point of the campaign

        Returns
        -------
        Response
            The HTTP Response
        """

        assert self._config is not None
        assert self._stage_graph is not None

        args_GET: list[str] = []
        for args_key in request.args.keys():
            args_GET.append(f"{args_key}={request.args[args_key]}")

        redirect_url: str = f"{self.get_entrypoint()}?{'&'.join(args_GET)}"
        return redirect(redirect_url)

    def get_entrypoint(self) -> str:
        return self._stage_graph.get_entry_point_local_url()

    def goto_admin_entrypoint(self) -> Response:
        """Generate the HTTP response to go to the admin entry point of the campaign

        Returns
        -------
        Response
            The HTTP Response
        """
        args_GET: list[str] = []
        for args_key in request.args.keys():
            args_GET.append(f"{args_key}={request.args[args_key]}")

        admin_module = self.register_admin_module(self._admin_entrypoint)
        redirect_url: str = f"/{admin_module.local_url()}/?{'&'.join(args_GET)}"
        return redirect(redirect_url)

    def register_stage_module(self, name: str, subname: str | None = None) -> StageModule:
        assert self._stage_graph is not None
        assert self._config is not None

        # Get the stage module and connect it to the stage graph
        module_name = name.replace("flexeval.mods.", "")
        stage_module = StageModule(namespace=module_name, subname=subname)
        self._stage_graph.connect_stage_module(module_name, stage_module)

        # Define the config of the module
        config: dict[str, Any] = self._config.get_module_config(module_name)
        stage_module.set_config(config)

        return stage_module

    def register_admin_module(self, name: str, subname: str | None = None) -> AdminModule:
        assert self._config is not None
        module = AdminModule(namespace=name.replace("flexeval.mods.", ""), subname=subname)
        config: dict[str, Any] = self._config.get_admin_config(name)
        module.set_config(config)
        self._admin_modules[name] = module
        return module

    def get_admin_modules(self) -> dict[str, AdminModule]:
        return self._admin_modules


campaign_instance: CampaignInstance = CampaignInstance()
