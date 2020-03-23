# Import Libraries
from flask import Blueprint

from core.utils import config,get_provider, render_template

bp = Blueprint('pages', __name__)

# Routes

@bp.route('/<name>', methods = ['GET'])
def get(name):

    if( config["stages"][name]["disconnect_user"]):
        try:
            get_provider("auth").destroy()
        except Exception as e:
            pass

    return render_template(config["stages"][name]["template"],stage_name=name)
