from flask import Blueprint, render_template,url_for,request,redirect,session
from mods.login.model.User import User as mUser
from utils import db,config

bp = Blueprint('pages', __name__,template_folder='templates',static_folder='../../static')

# Routes
@bp.route('/end')
def end():

    try:
        del session["user"]
    except Exception as e:
        pass

    return render_template('end.tpl')

@bp.route('/tuto')
def tuto():

    return render_template('tuto.tpl',next=config["pages"]["tuto"]["next"])
