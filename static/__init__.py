from flask import Blueprint, send_from_directory
import utils
import os

bp = Blueprint('assets', __name__)

# Routes
@bp.route('/<list:lpath>')
def get(lpath):

    path = ""

    for _path in lpath:
        if _path == "." or _path == ".." or _path == "~":
            return "BAD BOY"

        path = path + "/" + _path

    try:
        return send_from_directory(utils.NAME_REP_CONFIG+"./static",path)
    except Exception as e:
        try:
            return send_from_directory(utils.ROOT+"./static", path)
        except Exception as e:
            return ""
