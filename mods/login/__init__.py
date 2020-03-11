from flask import Blueprint, render_template,url_for,request,redirect,session
from mods.login.model.User import User as mUser
from utils import db,config

bp = Blueprint('login', __name__,template_folder='templates',static_folder='../../static')

# Routes
@bp.route('/')
def login():
    if "user" in session:
        return redirect(config["login"]["next"])
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

    return redirect(config["login"]["next"])
