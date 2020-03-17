from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config,NAME_REP_CONFIG,get_provider

bp = Blueprint('pages', __name__,template_folder=NAME_REP_CONFIG+'/templates')

# Routes

@bp.route('/<name>', methods = ['GET'])
def get(name):

    if( config["stages"][name]["deconnect_user"]):
        try:
            get_provider("auth").destroy()
        except Exception as e:
            pass

    next=None
    if "next" in config["stages"][name]:
        next=config["stages"][name]["next"]


    return render_template(config["stages"][name]["template"],next=next)
