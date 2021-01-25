# coding: utf8
# license : CeCILL-C

from flask import current_app

from flexeval.core import StageModule
from flexeval.database import Column, db
from flexeval.utils import redirect

with StageModule(__name__, subname="visitor") as sm:

    @sm.route("/", methods=["GET"])
    def main():
        stage = sm.current_stage
        authProvider = sm.authProvider

        if authProvider.validates_connection("connected")[0]:
            return sm.render_template(template=stage.template)

            # NOTE: the rediction is faulty as virtual leads to automatically to connected anonymous user
            # NOTE: Redirection based on remembering what was the last visited page

            # if stage.has_next_module():
            #     return redirect(stage.local_url_next)
            # else:
            #     return sm.render_template(template=stage.template)
        else:
            return sm.render_template(template=stage.template)


with StageModule(__name__, subname="user") as sm_user:

    @sm_user.route("/", methods=["GET"])
    @sm_user.valid_connection_required
    def main():
        stage = sm_user.current_stage
        user = sm_user.authProvider.user
        return sm.render_template(template=stage.template)
