"""
flexeval.core.Stage
===================

Module which defines all utilities to represent a stage in the pipeline

"""

from flask import g, abort
from flask import url_for as flask_url_for
from flask import session as flask_session

from flexeval.utils import make_global_url

from .Module import Module
from .Config import Config
from flexeval.core import ProviderFactory


class StageError(Exception):
    """Default exception if an error happens at a specific stage."""

    pass


class StageNotFound(StageError):
    """Exception raised if the wanted stage doesn't exist."""

    pass


class ResolvedStageTemplate:
    """Class which contains the path of the resolved template.

    This class is mainly here to distinguish strings which may need to
    be resolved to already resolved templates.

    Attributes
    ----------
    path: string
       The path to the faulty template

    """

    def __init__(self, template_path):
        self.path = template_path


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

    def __init__(self, name, data=None):
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
        self.name = name

        try:
            self.params = Config().data()["stages"][name]
        except Exception as e:
            raise StageNotFound()

        self.mod_name = self.params["type"]
        self.mod_rep = self.params["type"].split(":")[0]

    def update(self, name, val):
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

        if name not in Config().data()["stages"][self.name]:
            Config().data()["stages"][self.name][name] = None

        Config().data()["stages"][self.name][name] = val

    @property
    def session(self):
        """Method to retrieve the information associated with the current
        stage from the current session.

        This method is treated as a property.

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        dict: the session dictionnary

        """
        if "stage:" + self.name not in flask_session.keys():
            flask_session["stage:" + self.name] = {}

        return flask_session["stage:" + self.name]

    @property
    def local_url_next(self):
        """Method to retrieve the information associated with the current
        stage from the current session.

        This method is treated as a property.

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        dict: the session dictionnary
        """

        if "next" not in self.params:
            next_module = "/"
        else:

            if isinstance(self.params["next"], dict):
                next_module = {}
                for next_module_name in self.params["next"].keys():
                    next_module[next_module_name] = Stage(
                        self.params["next"][next_module_name]
                    ).local_url
            else:
                next_module = Stage(self.params["next"]).local_url

        return next_module

    def has_next_module(self):
        """Method which indicates if the current stage has a next module

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        bool: true if the module has a next module, false else
        """
        return "next" in self.params

    @property
    def template(self):
        """Method to get the template associated with the current stage.

        This method is treated as a property.

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        ResolvedStageTemplate: the resolved template

        """
        if "template" not in self.params:
            return None

        template = self.params["template"]
        template_path = ProviderFactory().get("templates").get(template)

        return ResolvedStageTemplate(template_path)

    @property
    def variables(self):
        """Method to get all the variables associated with the current stage.
        This also includes the session variables. Each variable is
        identified by a string name.

        This method is treated as a property.

        Parameters
        ----------
        self: self
            The current object

        Returns
        -------
        dict: the dictionnary of variables

        """
        variables = {}

        if "variables" in self.params:
            variables = self.params["variables"]

        if "session_variable" in self.session:
            for session_variable_name in self.session["session_variable"].keys():
                variables[session_variable_name] = self.session["session_variable"][
                    session_variable_name
                ]

        return variables

    def get_variable(self, name, default_value):
        """Method to get the value of a variable. If the variable is not
        available, the provided default value is returned.

        Parameters
        ----------
        self: Stage
            The current object
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

    def set_variable(self, name, value):
        """Method to set the value of a variable identified by its name.

        If the variable doesn't exist, a new SESSION variable will be created.

        Parameters
        ----------
        self: Stage
            The current object
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

        Parameters
        ----------
        self: Stage
            The current object

        Returns
        -------
        string: the URL of the current stage
        """
        return "/" + StageModule.name_type + "/" + self.mod_name + "/" + self.name + "/"

    def get(self, name):
        """Method to get the value of a parameter

        Parameters
        ----------
        self: Stage
            The current object
        name: string
            The name of the parameter of the current stage

        Returns
        -------
        object: The value of the parameter or None if the parameter doesn't exist
        """
        if name in self.params:
            return self.params[name]
        else:
            return None


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

    def local_rule(self):
        """Method which defines the rule to access the current module

        Parameters
        ----------
        self: StageModule
            The current object

        Returns
        -------
        string: the rule to access the current module
        """
        return (
            "/" + self.__class__.name_type + "/" + self.get_mod_name() + "/<stage_name>"
        )

    @property
    def current_stage(self):
        """Method which allows to access the current stage from the flask/Werkzeug proxy.

        This method is treated as a property.

        Parameters
        ----------
        self: StageModule
            The current object

        Returns
        -------
        Stage: the current stage
        """
        return g.stage

    def render_template(self, template, next=None, **parameters):
        """Method which renders the given template.

        As a stage

        """
        args = {}
        args["THIS_MODULE"] = "mod:" + str(self.mod_rep)

        # Save the URL of the next step
        if isinstance(self.current_stage.local_url_next, dict):
            global_url_next = {}
            for local_url_next_name in self.current_stage.local_url_next:
                global_url_next[local_url_next_name] = make_global_url(
                    self.current_stage.local_url_next[local_url_next_name]
                )
            args["url_next"] = global_url_next
        else:
            args["url_next"] = make_global_url(self.current_stage.local_url_next)

        # Get the template
        if isinstance(template, ResolvedStageTemplate):
            template = template.path
        else:
            template = ProviderFactory().get("templates").get(template)

        # Achieve the rendering
        return super().render_template(
            template,
            args=args,
            parameters=parameters,
            variables=self.current_stage.variables,
        )

    def url_for(self, endpoint, stage_name=None, **kwargs):
        """Method to generate a dynamic URL given a specific endpoint and
        potential stage name. If the stage name is None, the current
        stage name is used.

        Parameters
        ----------
        self: StageModule
            The current object
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

    def get_endpoint_for_local_rule(self, rule):
        """Method to generate the end point for the given local rule

        Parameters
        ----------
        self: StageModule
            The current object
        rule: string
            The rule

        Returns
        -------
        string: the generated endpoint
        """
        return self.name + "." + "local_url@" + str(rule.replace(".", "_"))

    def route(self, rule, **options):
        """Method to define the route decorator which will be in charge of
        redericting the client to the given rule.

        Parameters
        ----------
        self: StageModule
            The current object
        rule: string
            The rule which will be redirected too
        options: dict
            Additional options to pass to the redirection pipeline

        Returns
        -------
        ????: the routing decorator
        """

        def decorated(func):
            def wrapper(*args, **kwargs):
                stage_name = kwargs["stage_name"]
                del kwargs["stage_name"]

                self._logger.debug("Goto ==> %s" % stage_name)
                self._logger.debug("Current session:")
                for k in flask_session.keys():
                    self._logger.debug(" - %s: %s" % (k, flask_session[k]))
                try:
                    g.stage = Stage(stage_name)
                except Exception as e:
                    abort(404)

                return func(*args, **kwargs)

            self.add_url_rule(
                rule, "local_url@" + str(rule.replace(".", "_")), wrapper, **options
            )

            return wrapper

        return decorated
