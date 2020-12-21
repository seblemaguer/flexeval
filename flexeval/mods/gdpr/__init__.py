# coding: utf8
# license : CeCILL-C

# Global
import os
import logging

# Yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Flask
from flask import current_app
from flask import session as flask_session

# Flexeval
from flexeval.utils import AppSingleton, make_global_url, redirect
from flexeval.core import ProviderFactory, Module, Config
from flexeval.core.providers.auth import AuthProvider
from flexeval.core import StageModule
from flexeval.core import ErrorHandler

from .LegalTerms import LegalTerms, LegalTermNotCheckError

def check_validate_gdpr():
    LegalTerms().user_has_validate()

AuthProvider.connect_checker(check_validate_gdpr)

def legal_error_manager(error):
    stage_path = "/stage/gdpr/%s" % Config().get_stages("gdpr")[0]
    return LegalTerms().page_with_validation_required(stage_path)

ErrorHandler.add_error_manager(LegalTermNotCheckError, legal_error_manager)

with StageModule(__name__) as sm:

    @sm.route("/", methods=["GET"])
    def main():
        stage = sm.current_stage
        lg_terms = LegalTerms(stage.local_url_next)
        return lg_terms.page()
