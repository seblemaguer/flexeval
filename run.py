# Import Libraries
from flask import Flask,redirect,session, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import utils
import argparse
import os
from src.Assets import Assets
from src.Export import Export
import shutil
import traceback
import importlib

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
    def safe_copy_rep(SRC,DST):

        if not os.path.exists(DST):
            os.makedirs(DST)

        if os.path.exists(SRC):

            DST_files = os.listdir(DST)
            SRC_files = os.listdir(SRC)

            for file in SRC_files:
                if not(file in DST_files):
                    shutil.copyfile(SRC+"/"+file,DST+"/"+file)

    if os.path.exists(utils.NAME_REP_CONFIG+"/.tmp"):
        shutil.rmtree(utils.NAME_REP_CONFIG+"/.tmp")

    os.makedirs(utils.NAME_REP_CONFIG+"/.tmp")
    os.makedirs(utils.NAME_REP_CONFIG+"/.tmp/export_bdd")

    shutil.copytree(utils.NAME_REP_CONFIG+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")
    safe_copy_rep(utils.ROOT+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")

    # VARs
    activated_stage = []
    activated_mod = []

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

    utils.config = config
    utils.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+utils.NAME_REP_CONFIG+"/bdd_sqlite.db"
    utils.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    utils.app.secret_key = b'_5#y2zcer88L"Fczerzce4Q8sdqsdcezqtz\n\xec]/'
    utils.db = SQLAlchemy(utils.app)

    utils.assets = Assets("/assets")
    Export("/export")


    for mod in activated_mod:
        lib_imported = importlib.import_module("mods."+mod)
        utils.app.register_blueprint(lib_imported.bp,url_prefix='/'+str(mod)) # Register Blueprint
        safe_copy_rep(utils.ROOT+"/mods/"+mod+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/"+mod)

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

        return render_template('error.tpl',code=code,entrypoint=utils.config["entrypoint"])

    # Run app
    utils.app.run(host=args.host,port=args.port)
