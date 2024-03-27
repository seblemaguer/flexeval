from flexeval.core import campaign_instance

with campaign_instance.register_stage_module(__name__, subname="visitor") as sm:

    @sm.route("/", methods=["GET"])
    def main_visitor():
        stage = sm.current_stage
        authProvider = sm.auth_provider

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


with campaign_instance.register_stage_module(__name__, subname="user") as sm_user:

    @sm_user.route("/", methods=["GET"])
    @sm_user.valid_connection_required
    def main_user():
        stage = sm_user.current_stage
        return sm.render_template(template=stage.template)
