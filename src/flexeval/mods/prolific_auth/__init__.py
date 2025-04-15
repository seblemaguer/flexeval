# coding: utf8
# license : CeCILL-C

# Import Libraries
from flask import request

from flexeval.core import campaign_instance, StageModule
from flexeval.utils import redirect
import logging

from .provider import ProlificAuthProvider

StageModule.set_auth_provider(ProlificAuthProvider)

logger = logging.getLogger()

with campaign_instance.register_stage_module(__name__) as sm:

    @sm.route("/", methods=["GET"])
    def main():
        stage = sm.current_stage

        if sm.auth_provider.validates_connection("connected")[0]:
            next_urls: dict[str, str] = stage.next_local_urls
            if len(next_urls.keys()) > 1:
                raise Exception("Multiple next stages from the logging page are not yet supported")
            stage_name = list(next_urls.keys())[0]
            return redirect(next_urls[stage_name])
        else:
            return sm.render_template(path_template=stage.template)

    @sm.route("/register", methods=["POST"])
    def register():

        # Authenticate
        prolific_pid: str = request.form["PROLIFIC_PID"]
        study_id: str = request.form["STUDY_ID"]
        session_id: str = request.form["SESSION_ID"]

        if not prolific_pid:
            raise Exception("The participant ID is not defined")

        if not study_id:
            logger.warning("The study ID is not defined")

        if not session_id:
            logger.warning("The session ID is not defined")

        assert isinstance(sm.auth_provider, ProlificAuthProvider)
        sm.auth_provider.connect(prolific_pid, study_id, session_id)

        # Move to the next stage
        stage = sm.current_stage
        next_urls: dict[str, str] = stage.next_local_urls
        if len(next_urls.keys()) > 1:
            raise Exception("Multiple next stages from the logging page are not yet supported")
        stage_name = list(next_urls.keys())[0]
        return redirect(next_urls[stage_name])
