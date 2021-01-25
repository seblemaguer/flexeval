# coding: utf8
# license : CeCILL-C

# Flask
from flask import redirect
from flask import session as flask_session

# Flexeval
from flexeval.core.providers.auth import AuthProvider
from flexeval.core import StageModule

from .LegalTerms import LegalTerms

# Check the authentification
def check_validate_gdpr(user):
    return LegalTerms().user_has_validate()

AuthProvider.connect_checker("legal", check_validate_gdpr)

# Check the validation of the legal informations
def legal_error_manager(source_module):
    flask_session["source_url"] = source_module.current_stage.local_url
    return redirect('/stage/gdpr/validate_legal')

StageModule.connect_default_checker_handler("legal", legal_error_manager)

# Ready to serve!
with StageModule(__name__) as sm:

    @sm.route("/", methods=["GET"])
    def main():
        stage = sm.current_stage
        lg_terms = LegalTerms(stage.local_url_next)
        return lg_terms.page()
