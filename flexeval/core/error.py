# coding: utf8
# license : CeCILL-C

from typing import Any, ParamSpec
import logging
import traceback

from flask import render_template as flask_render_template
from flask import Flask
from werkzeug.exceptions import HTTPException

from flexeval.utils import make_global_url


from .providers import provider_factory, TemplateProvider, AssetsProvider
from .providers.auth import VirtualAuthProvider
from .Config import Config

P = ParamSpec("P")


class ErrorHandler:
    """Class which defines how errors are handled."""

    def __init__(self, app: Flask):
        """Constructor

        Parameters
        ----------
        self: ErrorHandler
            The current object
        """
        self._logger = logging.getLogger(self.__class__.__name__)

        # Define the default handler to be the method "error"
        app.register_error_handler(Exception, self.error)

    def error(self, e: Exception) -> str:
        """The error handler routine entry point.

        It is also in charge of execution the alternative handler, if one is defined for the type of error
        given in parameters.

        Parameters
        ----------
        self: ErrorHandler
            The current object
        e: Exception
            The exception to handle
        """

        # Deal with critical server errors
        code = 500
        if not (isinstance(e, HTTPException)):
            self._logger.critical('Error "%s"' % str(e))
            self._logger.critical("Traceback: ")
            for eline in traceback.format_exc().splitlines():
                self._logger.critical(eline)
        else:
            code: int | None = e.code

        variables: dict[str, Any] = Config().data()["variables"]  # type: ignore

        def _get_variable(key: str, *args: P.args, **kwargs: P.kwargs) -> Any:
            """Helper to replace a variable value in the template

            The variable can be a callable which will be ran and its
            returned value will be used

            Parameters
            ----------
            key : str
                the variable name/key

            Returns
            -------
            Any
                the obtained/computed value
            """

            default_value: Any | None = None
            if "default_value" in kwargs:
                default_value = kwargs["default_value"]

            if key in variables:
                return variables[key]
            else:
                return default_value

        def _get_asset(name: str, rep: str | None = None) -> str:
            asset_provider: AssetsProvider = provider_factory.get(AssetsProvider.NAME)  # type: ignore
            return make_global_url(asset_provider.local_url(name, rep))

        # Render the error page
        template_provider: TemplateProvider = provider_factory.get(TemplateProvider.NAME)  # type: ignore
        return flask_render_template(
            template_name_or_list=template_provider.get("error.tpl"),
            parameters={"code": code},
            get_template=provider_factory.get(TemplateProvider.NAME).get,  # type: ignore
            get_asset=_get_asset,
            get_variable=_get_variable,
            auth=VirtualAuthProvider(),
        )


error_handler: ErrorHandler | None = None
