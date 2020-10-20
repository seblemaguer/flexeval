# coding: utf8
# license : CeCILL-C

import logging
import traceback

from flask import current_app
from werkzeug.exceptions import HTTPException

from flexeval.utils import AppSingleton

from flexeval.core import ProviderFactory

from .LegalTerms import LegalTermNotCheckError, LegalTerms


class ErrorHandler(metaclass=AppSingleton):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        current_app.register_error_handler(Exception, self.error)

    def trace(self, e):
        code = 500
        if not (isinstance(e, HTTPException)):
            self._logger.critical("Error \"%s\"" % str(e))
            self._logger.critical("Traceback:" % str(e))
            for eline in traceback.format_exc().splitlines():
                self._logger.critical(eline)
        else:
            code = e.code

        return code

    def error(self, e):
        from .Module import Module

        if isinstance(e, LegalTermNotCheckError):
            return LegalTerms().page_with_validation_required("/")

        code = self.trace(e)
        return Module.render_template(
            ProviderFactory().get("templates").get("/error.tpl"),
            parameters={"code": code},
        )
