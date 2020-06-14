# coding: utf8
# license : CeCILL-C

import traceback

from flask import current_app
from werkzeug.exceptions import HTTPException

from flexeval.utils import AppSingleton
from .Provider import Provider

from .LegalTerms import LegalTermNotCheckError,LegalTerms

class ErrorHandler(metaclass=AppSingleton):

    def __init__(self):
        current_app.register_error_handler(Exception, self.error)

    def trace(e):
        code = 500
        if not(isinstance(e,HTTPException)):
            print("*******************************")
            print("A CRITICAL ERROR HAS OCCURED")
            print("")
            print("--> MSG")
            print(str(e))
            print("")
            print("--> TRACEBACK")
            for eline in traceback.format_exc().splitlines():
                print(eline)

            print("*******************************")
        else:
            code = e.code

        return code

    def error(self,e):
        from .Module import Module

        if isinstance(e,LegalTermNotCheckError):
            return LegalTerms().page_with_validation_required("/")

        code = ErrorHandler.trace(e)
        return Module.render_template(Provider().get("templates").get("/error.tpl","flexeval"),parameters={"code":code})
