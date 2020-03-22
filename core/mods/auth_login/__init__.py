# Import Libraries
from flask import Blueprint,request,redirect,session, render_template

from core.mods.auth_login.model.User import User as mUser
from core.mods.auth_login.src.LoginProvider import LoginAuthProvider
from core.utils import db,config,get_provider,set_provider

bp = Blueprint('auth_login', __name__)
set_provider("auth",LoginAuthProvider())

# Routes
@bp.route('/<name>')
def login(name):
    if "user" in session:
        return redirect(config["stages"][name]["next"])
    else:
        return render_template('auth_login/login.tpl',userprov=get_provider("auth"),name=name)

@bp.route('/<name>/log-register', methods = ['POST'])
def log_register(name):
    email =  request.form["email"]

    try:
        user = mUser.query.filter_by(email=email).first()
        assert not(user is None)
    except Exception as e:
        user = mUser(email)
        db.session.add(user)
        db.session.commit()

    get_provider("auth").set(user.email)

    return redirect(config["stages"][name]["next"])
