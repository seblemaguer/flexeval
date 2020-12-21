# coding: utf8
# license : CeCILL-C

import logging
import traceback

from flask import current_app
from werkzeug.exceptions import HTTPException

from flexeval.core import ProviderFactory
from flexeval.utils import AppSingleton

from .Module import Module


class ErrorHandler(metaclass=AppSingleton):
    error_managers = dict()
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        current_app.register_error_handler(Exception, self.error)

    def trace(self, e):
        code = 500
        if not (isinstance(e, HTTPException)):
            self._logger.critical("Error \"%s\"" % str(e))
            self._logger.critical("Traceback: ")
            for eline in traceback.format_exc().splitlines():
                self._logger.critical(eline)
        else:
            code = e.code

        return code

    @classmethod
    def add_error_manager(cls, error_class, error_manager):
        ErrorHandler.error_managers[error_class] = error_manager

    def error(self, e):
        error_class = None
        for cur_error_class in ErrorHandler.error_managers.keys():
            if isinstance(e, cur_error_class):
                error_class = cur_error_class
                break

        if error_class is not None:
            return ErrorHandler.error_managers[error_class](e)

        code = self.trace(e)
        return Module.render_template(
            ProviderFactory().get("templates").get("/error.tpl"),
            parameters={"code": code},
        )
