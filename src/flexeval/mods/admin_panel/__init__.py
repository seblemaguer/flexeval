# coding: utf8
# license : CeCILL-C

from typing import Any
from flask import request

from flexeval.core import campaign_instance
from flexeval.core import AdminModule
from flexeval.utils import redirect, make_global_url

from .provider import UniqueAuth

AdminModule.set_auth_provider(UniqueAuth)

with campaign_instance.register_admin_module(__name__) as am:

    @am.route("/", methods=["GET"])
    def main():
        authProvider = am.auth_provider

        if authProvider.validates_connection("connected")[0]:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/panel")))
        else:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/auth")))

    @am.route("/auth", methods=["GET"])
    def auth():
        return am.render_template(path_template="auth.tpl")

    @am.route("/login", methods=["POST"])
    def login():
        password = request.form["admin_password"]
        master_password = am.get_config()["password"]

        if password == master_password:
            am.auth_provider.connect()
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/panel")))
        else:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/")))

    @am.route("/panel", methods=["GET"])
    @am.valid_connection_required
    def panel():
        admin_modules = []

        for mod_name, mod in campaign_instance.get_admin_modules().items():
            if am != mod:
                config_mod = mod.get_config()
                title = mod_name
                description = ""
                if "variables" in config_mod:
                    if "subtitle" in config_mod["variables"]:
                        title = config_mod["variables"]["subtitle"]

                    if "subdescription" in config_mod["variables"]:
                        description = config_mod["variables"]["subdescription"]

                admin_module = {
                    "title": title,
                    "description": description,
                    "url": make_global_url("/" + mod.local_url()),
                }

                admin_modules.append(admin_module)

        variables: dict[str, Any] = dict()
        variables["admin_modules"] = admin_modules
        return am.render_template(path_template="panel.tpl", variables=variables)
