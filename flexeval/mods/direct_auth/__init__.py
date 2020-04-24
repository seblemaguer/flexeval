# coding: utf8
# license : CeCILL-C

# Import Libraries
from flask import current_app, request

from flexeval.core import StageModule
from flexeval.utils import redirect

from .provider import EmailAuth
from .model import NotAnEmail

StageModule.set_authProvider(EmailAuth)

with StageModule(__name__) as sm:

    @sm.route("/", methods = ['GET'])
    def main():
        stage = sm.current_stage

        if(sm.authProvider.is_connected):
            return redirect(stage.local_url_next)
        else:
            return sm.render_template(template="login.tpl")

    @sm.route("/register",methods = ['POST'])
    def register():

        stage = sm.current_stage
        email = request.form["email"]

        try:
            sm.authProvider.connect(email)
        except NotAnEmail as e:
            return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

        return redirect(stage.local_url_next)
