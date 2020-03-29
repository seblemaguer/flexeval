# Import Libraries
from flask import Blueprint,request,redirect,session,abort

from core.mods.auth_login.model.User import User as mUser
from core.src.providers.AuthProvider import LoginAuthProvider
from core.utils import db,config,get_provider,set_provider,render_template
from core.src.Module import StageModule

set_provider("auth",LoginAuthProvider())

with StageModule('auth_login', __name__, requiere_auth=False) as bp:

    # Routes
    @bp.route('/<name>')
    def login(name):

        if(name not in config["stages"]):
            abort(404)

        if "user" in session:
            return redirect(config["stages"][name]["next"])
        else:
            return render_template('auth_login/login.tpl',stage_name=name)

    @bp.route('/<name>/log-register', methods = ['POST'])
    def log_register(name):
        email =  request.form["email"]

        if(name not in config["stages"]):
            abort(404)

        try:
            user = mUser.query.filter_by(email=email).first()
            assert not(user is None)
        except Exception as e:
            user = mUser(email)
            db.session.add(user)
            db.session.commit()

        get_provider("auth").set(user.email)

        return redirect(config["stages"][name]["next"])
