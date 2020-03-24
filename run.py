# Import Libraries
import json
import argparse
import os
import shutil
import traceback
import importlib

from flask import Flask,redirect
from flask_sqlalchemy import SQLAlchemy

from core.src.Assets import Assets
from core.src.Export import Export
import core.utils as utils

#  Main
if __name__ == '__main__':

    # Arguments Parsing
    parser = argparse.ArgumentParser(description='PercEval')
    parser.add_argument("instance",metavar='NAME_INST', type=str, help='instance\'s name')
    parser.add_argument("host",metavar='HOST', type=str, help='127.0.0.1')
    parser.add_argument("port",metavar='PORT', type=int, help='8080')
    args = parser.parse_args()

    utils.ROOT =  os.path.dirname(os.path.abspath(__file__))
    utils.NAME_REP_CONFIG = os.path.dirname(os.path.abspath(__file__))+"/instances/"+args.instance

    utils.app = Flask(__name__,template_folder = utils.NAME_REP_CONFIG+"/.tmp/templates",static_url_path=None)

    # Template
    if os.path.exists(utils.NAME_REP_CONFIG+"/.tmp"):
        shutil.rmtree(utils.NAME_REP_CONFIG+"/.tmp")

    os.makedirs(utils.NAME_REP_CONFIG+"/.tmp")
    os.makedirs(utils.NAME_REP_CONFIG+"/.tmp/export_bdd")

    utils.safe_copy_rep(utils.NAME_REP_CONFIG+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")
    utils.safe_copy_rep(utils.ROOT+"/core/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")
    utils.safe_copy_rep(utils.ROOT+"/core/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/core")

    # VARs
    activated_stage = []
    activated_mod = []

    try:
        with open(utils.NAME_REP_CONFIG+'/structure.json') as config:
            config = json.load(config)


             #lOAD
            next_stage_name = config["entrypoint"]
            next_stage = config["stages"][next_stage_name]

            # REWRITE
            config["entrypoint"] = "/"+next_stage["type"]+"/"+ next_stage_name
            activated_stage.append("entrypoint")

            while not(next_stage is None):

                current = next_stage

                # Activate mods (attr type)
                if not(current["type"] in activated_mod):
                    mod = current["type"]
                    activated_mod.append(mod)

                if "turn_next" in current:
                    turn_next = config["stages"][current["turn_next"]]
                    current["turn_next"] = "/"+turn_next["type"]+"/"+ current["turn_next"]

                # Next stage ? (attr next)
                if "next" in current:
                    if current["next"] in config["stages"]:
                        next_stage = config["stages"][current["next"]]

                        # REWRITE
                        current["next"] =  "/"+next_stage["type"]+"/"+ current["next"]
                    else:
                        next_stage = None
                else:
                    next_stage = None
    except Exception as e:
        raise Exception("Issue in structure.json")

    utils.config = config
    utils.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+utils.NAME_REP_CONFIG+"/bdd_sqlite.db"
    utils.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    utils.app.secret_key = b'_5#y2zcer88L"Fczerzce4Q8sdqsdcezqtz\n\xec]/'
    utils.db = SQLAlchemy(utils.app)

    utils.assets = Assets("/assets")
    Export("/export")

    for mod in activated_mod:
        lib_imported = importlib.import_module("core.mods."+mod)
        utils.app.register_blueprint(lib_imported.bp,url_prefix='/'+str(mod)) # Register Blueprint
        utils.safe_copy_rep(utils.ROOT+"/core/mods/"+mod+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/"+mod)

    utils.db.create_all()

    @utils.app.route('/')
    def main_route():
        return redirect(utils.config["entrypoint"])

    @utils.app.route('/deco')
    def deco():
        try:
            utils.get_provider("auth").destroy()
        except Exception as e:
            pass

        return redirect(utils.config["entrypoint"])


    @utils.app.errorhandler(Exception)
    def not_found(e):
        print("*******************************")
        print("A CRITICAL ERROR HAS OCCURED")
        print("")
        print("--> MSG")
        print(str(e))
        print("")
        print("--> TRACEBACK")
        for eline in traceback.format_exc().splitlines():
            print(eline)

        print("*******************************")
        try:
            code = e.code
        except Exception as e:
            code = 500

        try:
            utils.get_provider("auth").destroy()
        except Exception as e:
            pass

        return utils.render_template('error.tpl',code=code,entrypoint=utils.config["entrypoint"])

    # Run app
    utils.app.run(host=args.host,port=args.port)
