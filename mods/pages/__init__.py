from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config,NAME_REP_CONFIG

bp = Blueprint('pages', __name__,template_folder=NAME_REP_CONFIG+'/templates',static_folder='../../assets')

# Routes

@bp.route('/<name>', methods = ['GET'])
def get(name):

    return render_template(config["pages"][name]["template"],next=config["pages"][name]["next"])
