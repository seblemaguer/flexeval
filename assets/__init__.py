from flask import Blueprint, send_from_directory, abort
import utils
import os

bp = Blueprint('assets', __name__)

# Routes
@bp.route('/<path:lpath>')
def get(lpath):

    try:
        lpath = lpath.split("/")

        file = lpath[len(lpath)-1]
        lpath = lpath[:len(lpath)-1]

        path = ""

        assert not(file == "." or file == ".." or file == "~")

        for _path in lpath:
            assert not(_path == "." or _path == ".." or _path == "~")

            path = path + "/" + _path

        try:
            return send_from_directory(utils.NAME_REP_CONFIG+"/assets"+path,file)
        except Exception as e:
            return send_from_directory(utils.ROOT+"/assets"+path, file)
    except Exception as e:
        abort(404)
