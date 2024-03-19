# coding: utf8
# license : CeCILL-C

import logging
import traceback

from flask import current_app
from werkzeug.exceptions import HTTPException

from flexeval.core.providers import provider_factory
from flexeval.utils import AppSingleton

from .Module import Module


class ErrorHandler(metaclass=AppSingleton):
    """Class which defines how errors are handled.

    Class Attributes
    ==========
    error_alternative_handlers: dict of <Error Class> => function(error: <Error Class>)
       Dictionnary which provides an alternative handler for a specific error which is of type Error Class
    """

    error_alternative_handlers = dict()

    @classmethod
    def add_alternative_handler(cls, error_class, error_alternative_handler):
        """Add a new handler for a given error class

        Parameters
        ----------
        cls: Class
            the class ErrorHandler
        error_class: Class
            The error class
        error_alternative_handler: function(error: <Error Class>)
            The alternative handler
        """
        ErrorHandler.error_alternative_handlers[error_class] = error_alternative_handler

    def __init__(self):
        """Constructor

        Parameters
        ----------
        self: ErrorHandler
            The current object
        """
        self._logger = logging.getLogger(self.__class__.__name__)

        # Define the default handler to be the method "error"
        current_app.register_error_handler(Exception, self.error)

    def error(self, e):
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
            code = e.code

        # Render the error page
        return Module.render_template(
            provider_factory.get("templates").get("error.tpl"),
            parameters={"code": code},
        )
