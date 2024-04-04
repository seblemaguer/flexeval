# coding: utf8
# license : CeCILL-C

# Import Libraries
from flask import request

from flexeval.core import campaign_instance, StageModule
from flexeval.utils import redirect

from .provider import ProlificAuth

StageModule.set_auth_provider(ProlificAuth)


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
        # Authenticate
        user_id: str = request.form["USER_ID"]
        study_id: str = request.form["STUDY_ID"]
        session_id: str = request.form["SESSION_ID"]
        sm.auth_provider.connect(user_id, study_id, session_id)

        # Move to the next stage
        stage = sm.current_stage
        next_urls: dict[str, str] = stage.next_local_urls
        if len(next_urls.keys()) > 1:
            raise Exception("")
        stage_name = list(next_urls.keys())[0]
        return redirect(next_urls[stage_name])
