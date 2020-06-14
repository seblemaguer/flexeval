# coding: utf8
# license : CeCILL-C

from flask import current_app, request

from flexeval.core import AdminModule
from flexeval.utils import redirect,make_global_url

from .provider import UniqueAuth

AdminModule.set_authProvider(UniqueAuth)

with AdminModule(__name__) as am:

    @am.route("/", methods = ['GET'])
    def main():
        authProvider = am.authProvider

        if authProvider.is_connected:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/panel")))
        else:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/auth")))


    @am.route("/auth", methods = ['GET'])
    def auth():
        return am.render_template(template="auth.tpl")

    @am.route("/login", methods = ['POST'])
    def login():
        password = request.form["admin_password"]
        master_password = am.get_config()["password"]

        if password == master_password:
            am.authProvider.connect()
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/panel")))
        else:
            return redirect(am.url_for(am.get_endpoint_for_local_rule("/")))


    @am.route("/panel", methods = ['GET'])
    @am.connection_required
    def panel():

        admin_modules=[]

        for mod in AdminModule.get_all_admin_modules():
            if not(am.get_mod_name() == mod["mod"]):
                title = mod["mod"]
                description = ""
                if "variables" in mod:

                    if "subtitle" in mod["variables"]:
                        title = mod["variables"]["subtitle"]

                    if "subdescription" in mod["variables"]:
                        description = mod["variables"]["subdescription"]

                admin_module = {
                                    "title":title,
                                    "description":description,
                                    "url":make_global_url(AdminModule.get_local_url_for(mod["mod"]))
                                }

                admin_modules.append(admin_module)

        return am.render_template(template="panel.tpl",admin_modules=admin_modules)
