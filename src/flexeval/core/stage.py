"""
flexeval.core.Stage
===================

Module which defines all utilities to represent a stage in the pipeline

"""

from typing import Any, Callable, ParamSpec
from typing_extensions import override

from flask import g as flask_global
from flask import url_for as flask_url_for
from flask import session as flask_session

from flexeval.utils import make_global_url

from .module import Module
from .providers import provider_factory, TemplateProvider

P = ParamSpec("P")


class StageError(Exception):
    """Default exception if an error happens at a specific stage."""

    pass


class StageNotFound(StageError):
    """Exception raised if the wanted stage doesn't exist."""

    pass


class Stage:
    """Definition of a stage submodule. It doesn't derive from the Module
    class but have a lot in common with it.

    Attributes
    ----------
    name: string
       The name of the stage
    params: ???
       The parameters needed by the stage to be executed properly
    mod_name: string
       The name of the module of the stage (????)
    mod_rep: string
       the  ???? of the module of the stage (???)
    """

    def __init__(self, name: str, config: dict[str, Any]):
        """Constructor

        Parameters
        ----------
        self: Stage
            The current object
        name: string
            The name of the stage
        data: None
            Not used (FIXME: check)
        """
        self.name: str = name
        self._config = config
        self._next_stages: dict[str, Stage] = dict()

        self._mod_name: str = self._config["type"]
        self._mod_rep: str = self._config["type"].split(":")[0]

        # Get rid of unwanted keywords (FIXME: it should not be there)
        del self._config["type"]
        if "next" in self._config:
            del self._config["next"]

    def add_next_stage(self, stage_name: str, stage):
        self._next_stages[stage_name] = stage

    @property
    def mod_rep(self) -> str:
        return self._mod_rep

    def update(self, name: str, val: object):
        """Method to update the value of a parameter of the stage

        Parameters
        ----------
        self: Stage
            The current object
        name: string
            The name of the parameter to update
        val: object
            The value of the parameter to update

        Raises
        ------
        AssertionError if name value is "type" or "name"
        """
        assert not (name == "type") and not (name == "name")

        if name not in self._config:
            self._config[name] = None

        self._config[name] = val

    @property
    def session(self):
        """Method to retrieve the information associated with the current
        stage from the current session.

        This method is treated as a property.

        Returns
        -------
        dict: the session dictionnary

        """
        if "stage:" + self.name not in flask_session.keys():
            flask_session["stage:" + self.name] = {}

        return flask_session["stage:" + self.name]

    @property
    def next_local_urls(self) -> dict[str, str]:
        """Generates the local URL of the next stage (treated a property)"""

        next_stage_urls: dict[str, str] = dict()

        for next_stage_name, next_stage in self._next_stages.items():
            next_stage_urls[next_stage_name] = next_stage.local_url

        return next_stage_urls

    def has_next_stage(self):
        """Method which indicates if the current stage has a next module

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        bool: true if the module has a next module, false else
        """
        return self._next_stages

    @property
    def template(self) -> str | None:
        """Method to get the template associated with the current stage.

        This method is treated as a property.

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        str | None: the template name/subpath or None

        """
        if "template" not in self._config:
            return None

        template = self._config["template"]
        template_path = provider_factory.get(TemplateProvider.NAME).get(template)
        return template_path

    @property
    def variables(self) -> dict[str, Any]:
        """Method to get all the variables associated with the current stage.
        This also includes the session variables. Each variable is
        identified by a string name.

        This method is treated as a property.

        Returns
        -------
        dict: the dictionnary of variables

        """
        variables: dict[str, Any] = dict()

        if "variables" in self._config:
            variables = self._config["variables"]

        if "session_variable" in self.session:
            for session_variable_name in self.session["session_variable"].keys():
                variables[session_variable_name] = self.session["session_variable"][session_variable_name]

        return variables

    def get_variable(self, name: str, default_value: object) -> object:
        """Method to get the value of a variable. If the variable is not
        available, the provided default value is returned.

        Parameters
        ----------
        name: string
            The name of the variable
        default_value: object
            The default value to return if the variable is not available

        Returns
        -------
        object: the value of the variable, if present, the default value else

        """
        if not (name in self.variables):
            return default_value

        return self.variables[name]

    def set_variable(self, name: str, value: object):
        """Method to set the value of a variable identified by its name.

        If the variable doesn't exist, a new SESSION variable will be created.

        Parameters
        ----------
        name: string
            The name of the variable
        value: object
            The new value of the variable

        """
        if not ("session_variable" in self.session):
            self.session["session_variable"] = {}
        self.session["session_variable"][name] = value

    @property
    def local_url(self):
        """Method to generate the URL of the current stage

        This method is treated as a property.

        Returns
        -------
        string: the URL of the current stage
        """
        return "/" + StageModule.name_type + "/" + self._mod_name + "/" + self.name + "/"

    def get(self, name: str) -> str | None:
        """Method to get the value of a parameter

        Parameters
        ----------
        name: string
            The name of the parameter of the current stage

        Returns
        -------
        object: The value of the parameter or None if the parameter doesn't exist
        """
        if name in self._config:
            return self._config[name]
        else:
            return None

    def has(self, name: str) -> bool:
        """Method to check if the value of a parameter is set

        Parameters
        ----------
        name: string
            The name of the parameter of the current stage

        Returns
        -------
        boolean: True if the parameter exists and has a value, False else
        """
        return name in self._config

    @override
    def __str__(self) -> str:
        str_rep = f"Stage({self.name}, {self._mod_name})\n"
        str_rep += f"\t- config = {self._config}\n"
        str_rep += f"\t- next_stages = {self._next_stages}"
        return str_rep


class StageModule(Module):
    """Class which defines the entry point of a stage.

    A stage is composed of substages which are instance of the class Stage.

    Attributes
    ----------
    current_stage: Stage
         The current substage
    """

    name_type = "stage"
    homepage = "/"

    def __init__(self, namespace: str, subname: str | None = None):
        super().__init__(namespace, subname)
        self._stages: dict[str, Stage] = dict()

    def add_stage(self, stage_name: str, stage: Stage):
        self._stages[stage_name] = stage

    @override
    def local_rule(self) -> str:
        """Method which defines the rule to access the current module

        Returns
        -------
        string: the rule to access the current module
        """
        return "/" + self.__class__.name_type + "/" + self.get_mod_name() + "/<stage_name>"

    @property
    def current_stage(self) -> Stage:
        """Method which allows to access the current stage from the flask/Werkzeug proxy.

        This method is treated as a property.

        Returns
        -------
        Stage: the current stage
        """
        return flask_global.stage

    # FIXME: invalid override
    @override
    def render_template(
        self,
        path_template: str | None = None,
        args: dict[str, Any] = dict(),
        variables: dict[str, Any] = dict(),
        parameters: dict[str, Any] = dict(),
    ) -> str:
        """Method which renders the given template."""
        internal_args: dict[str, Any] = dict()
        internal_args["THIS_MODULE"] = "mod:" + str(self.mod_rep)

        # Save the URL of the next step
        global_url_next: dict[str, str] = dict()
        if len(self.current_stage.next_local_urls.keys()) > 1:
            for local_url_next_name, local_url_next in self.current_stage.next_local_urls.items():
                global_url_next[local_url_next_name] = make_global_url(local_url_next)

        elif len(self.current_stage.next_local_urls.keys()) == 1:
            local_url_next = next(iter(self.current_stage.next_local_urls.values()))
            global_url_next["default"] = make_global_url(local_url_next)
            internal_args["url_next"] = global_url_next

        # Achieve the rendering
        return super().render_template(
            path_template,
            args=internal_args,
            parameters=parameters,
            variables=self._config["variables"],
        )

    @override
    def url_for(self, endpoint: str, stage_name: str | None = None, **kwargs) -> str:  # type: ignore
        """Method to generate a dynamic URL given a specific endpoint and
        potential stage name. If the stage name is None, the current
        stage name is used.

        Parameters
        ----------
        endpoint: string
            the end point
        stage_name: string
            The name of the stage
        kwargs: dict
            Any additionnal parameters which should be forwarded

        Returns
        -------
        string: the generated URL
        """

        if stage_name is None:
            stage_name = self.current_stage.name

        return flask_url_for(endpoint, stage_name=stage_name, **kwargs)

    def get_endpoint_for_local_rule(self, rule: str) -> str:
        """Method to generate the end point for the given local rule

        Parameters
        ----------
        rule: string
            The rule

        Returns
        -------
        string: the generated endpoint
        """
        return f"{self.name}.local_url@{rule.replace('.', '_')}"

    @override
    def route(self, rule: str, **options: Any) -> Callable[..., Any]:
        """Method to define the route decorator which will be in charge of
        redericting the client to the given rule.

        Parameters
        ----------
        rule: str
            The rule which will be redirected too
        options: dict
            Additional options to pass to the redirection pipeline

        Returns
        -------
        Callable[..., Any]
            The wrapping function
        """

        def decorated(lambda_fun: Callable[P, Any]) -> Any:
            def view_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                # Retrieve the stage name AND do NOT propagate it!
                stage_name: str = str(kwargs["stage_name"])
                del kwargs["stage_name"]

                # Just some nice debugging information to determine where we are
                self._logger.debug("Goto ==> %s" % stage_name)
                self._logger.debug("Current session:")
                for k in flask_session.keys():
                    self._logger.debug(" - %s: %s" % (k, flask_session[k]))

                # Define the the current stage
                flask_global.stage = self._stages[stage_name]

                return lambda_fun(*args, **kwargs)

            self.add_url_rule(rule, f"local_url@{rule.replace('.', '_')}", view_wrapper, **options)

            return view_wrapper

        return decorated

    @property
    def logger(self):
        return self._logger


class StageGraph:
    def __init__(self, entry_point: str, list_stages: list[str], stage_configs: dict[str, Any]):
        self._entry_point: str = entry_point
        self._dependency_graph: dict[str, list[str]] = dict()
        self._dict_stages: dict[str, Stage] = dict()

        self._load_stages(list_stages, stage_configs)

    def connect_stage_module(self, module_name: str, module: StageModule):
        for stage_name, stage in self._dict_stages.items():
            if stage.mod_rep == module_name:
                module.add_stage(stage_name, stage)

    def _load_stages(self, list_stages: list[str], stage_configs: dict[str, Any]):

        # Generate dependency graph
        for stage_name in list_stages:
            cur_stage_config = stage_configs[stage_name]
            if "next" in cur_stage_config:
                self._dependency_graph[stage_name] = cur_stage_config["next"]

        # Instanciate the stages
        for stage_name in list_stages:
            self._dict_stages[stage_name] = Stage(stage_name, stage_configs[stage_name])

        # Now define the dependencies
        for stage_name in list_stages:
            if stage_name in self._dependency_graph.keys():
                for next_stage in self._dependency_graph[stage_name]:
                    self._dict_stages[stage_name].add_next_stage(next_stage, self._dict_stages[next_stage])

    def get_stage(self, stage_name: str) -> Stage:
        return self._dict_stages[stage_name]

    def has_next_stage(self, stage_name: str) -> bool:
        return (stage_name in self._dependency_graph.keys()) and (len(self._dependency_graph[stage_name]) > 0)

    def get_next_stages(self, stage_name: str) -> list[Stage]:
        assert self.has_next_stage(stage_name)

        # Get the names first
        next_stages: list[Stage] = []
        for next_stage_name in self._dependency_graph[stage_name]:
            cur_stage: Stage = self._dict_stages[next_stage_name]
            next_stages.append(cur_stage)

        return next_stages

    def get_entry_point_local_url(self) -> str:
        return self._dict_stages[self._entry_point].local_url

    def list_stages(self) -> dict[str, Stage]:
        return self._dict_stages
