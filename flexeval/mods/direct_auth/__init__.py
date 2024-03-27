# coding: utf8
# license : CeCILL-C

# Import Libraries
from flask import request

from flexeval.core import campaign_instance, StageModule
from flexeval.utils import redirect

from .provider import EmailAuth
from .model import NotAnEmail

StageModule.set_auth_provider(EmailAuth)


with campaign_instance.register_stage_module(__name__) as sm:

    @sm.route("/", methods=["GET"])
    def main():
        stage = sm.current_stage

        if sm.auth_provider.validates_connection("connected")[0]:

            next_urls: dict[str, str] = stage.next_local_urls
            if len(next_urls.keys()) > 1:
                raise Exception("")
            stage_name = list(next_urls.keys())[0]
            return redirect(next_urls[stage_name])
        else:
            return sm.render_template(template="login.tpl")

    @sm.route("/register", methods=["POST"])
    def register():
        stage = sm.current_stage
        email: str = request.form["email"]

        try:
            sm.auth_provider.connect(email)
        except NotAnEmail as e:
            sm.logger.error(f"Problem with the email: {e}")
            return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

        next_urls: dict[str, str] = stage.next_local_urls
        if len(next_urls.keys()) > 1:
            raise Exception("")
        stage_name = list(next_urls.keys())[0]
        return redirect(next_urls[stage_name])
