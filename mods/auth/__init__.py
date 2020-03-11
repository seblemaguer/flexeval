from flask import Blueprint, render_template,url_for,request,redirect,session
from mods.auth.model.User import User as mUser
from utils import db,config

bp = Blueprint('auth', __name__,template_folder='templates',static_folder='../../assets')

# Routes
@bp.route('/login')
def login():
    if "user" in session:
        return redirect(config["auth"]["login"]["next"])
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

    session["user"] = user.id

    return redirect(config["auth"]["login"]["next"])

@bp.route('/deco/<name>')
def deco(name):
    try:
        del session["user"]
    except Exception as e:
        pass

    return redirect(config["auth"]["deco"][name]["next"])
