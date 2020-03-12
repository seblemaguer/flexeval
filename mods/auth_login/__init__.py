from flask import Blueprint, render_template,url_for,request,redirect,session
from mods.auth_login.model.User import User as mUser
from mods.auth_login.src.LoginProvider import LoginAuthProvider
from utils import db,config,get_provider,set_provider

bp = Blueprint('auth_login', __name__,template_folder='templates',static_folder='../../assets')
set_provider("auth",LoginAuthProvider())

# Routes
@bp.route('/login')
def login():
    if "user" in session:
        return redirect(config["auth_login"]["login"]["next"])
    else:
        return render_template('login.tpl')

@bp.route('/log-register', methods = ['POST'])
def log_register():
    email =  request.form["email"]

    try:
        user = mUser.query.filter_by(email=email).first()
        assert not(user is None)
    except Exception as e:
        user = mUser(email)
        db.session.add(user)
        db.session.commit()

    get_provider("auth").set(user.id)

    return redirect(config["auth_login"]["login"]["next"])

@bp.route('/deco/<name>')
def deco(name):
    try:
        get_provider("auth").destroy()
    except Exception as e:
        pass

    return redirect(config["auth_login"]["deco"][name]["next"])
