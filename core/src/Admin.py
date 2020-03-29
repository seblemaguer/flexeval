# Import Libraries
import os
import importlib

from flask import Blueprint,request,redirect,session, abort

from core.utils import config, render_template, app, admin_mod,reserved_name, NAME_REP_CONFIG, ROOT, make_url


class AdminPanel():

    def __init__(self):
        reserved_name.append("admin")
        reserved_name.append("deco")
        reserved_name.append("auth")

        app.add_url_rule('/admin/','admin_login',self.panel,methods=["POST","GET"])
        app.add_url_rule('/admin/deco','admin_deco',self.deco,methods=["POST","GET"])
        app.add_url_rule('/admin/auth','admin_auth',self.auth,methods=["POST","GET"])


    def authorize(func):
        def authorize_and_call(*args, **kwargs):
            if "admin_password" in request.form:
                session["admin_password"] = request.form["admin_password"]

            if "admin_password" in session:
                if not(session["admin_password"] == config["admin"]["password"]):
                    del session["admin_password"]
                    abort(401)
            else:
                return redirect(make_url("/admin/auth"))

            return func(*args, **kwargs)
        return authorize_and_call


    def auth(self):
        return render_template("admin/auth.tpl")

    @authorize
    def panel(self):
        tiles = []

        for it_admin_mod  in admin_mod:
            tiles.append({"title":it_admin_mod.TITLE,"description":it_admin_mod.DESCRIPTION,"link":"./"+it_admin_mod.mod_name})

        return render_template("admin/panel.tpl",tiles=tiles)

    @authorize
    def deco(self):
        del session["admin_password"]
        return redirect("./")
