# Import Libraries
from flask import Blueprint, abort

from core.utils import config,get_provider, render_template

bp = Blueprint('page', __name__)

# Routes

@bp.route('/<name>', methods = ['GET'])
def get(name):

    if(name not in config["stages"]):
        abort(404)

    if( config["stages"][name]["disconnect_user"]):
        try:
            get_provider("auth").destroy()
        except Exception as e:
            pass

    return render_template(config["stages"][name]["template"],stage_name=name)
