# Import Libraries
from flask import Blueprint, abort

from core.utils import config,get_provider, render_template
from core.src.Module import StageModule

with StageModule('questionnaire', __name__,requiere_auth=False) as bp:

    # Routes
    @bp.route('/<name>', methods = ['GET'])
    def get(name):

        if(name not in config["stages"]):
            abort(404)

        try:
            if( config["stages"][name]["disconnect_user"]):
                get_provider("auth").destroy()
        except Exception as e:
            pass

        username = ""
        if "requiere_auth" in config["stages"][name]:
            if config["stages"][name]["requiere_auth"]:
                username = get_provider("auth").get()

        return render_template(config["stages"][name]["template"],stage_name=name,username=username)
