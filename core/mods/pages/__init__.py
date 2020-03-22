# Import Libraries
from flask import Blueprint, render_template

from core.utils import config,get_provider

bp = Blueprint('pages', __name__)

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

    _parameters = None
    if "parameters" in config["stages"][name]:
        _parameters=config["stages"][name]["parameters"]

    return render_template(config["stages"][name]["template"],userprov=get_provider("auth"),next=next,parameters=_parameters)
