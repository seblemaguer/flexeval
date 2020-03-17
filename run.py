# Import Libraries
from flask import Flask,redirect,session, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import utils
import argparse
import os
import static as sstatic
import shutil

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

    utils.app = Flask(__name__,template_folder = utils.NAME_REP_CONFIG+"/.tmp/templates")

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
    shutil.copytree(utils.NAME_REP_CONFIG+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")
    safe_copy_rep(utils.ROOT+"/templates",utils.NAME_REP_CONFIG+"/.tmp/templates")

    active_mods = []
    with open(utils.NAME_REP_CONFIG+'/structure.json') as config:
        config = json.load(config)
        name = config["entrypoint"]
        intel = config["stages"][name]
        config["entrypoint"] = "/"+intel["type"]+"/"+ name

        for stage in config["stages"]:
            active_mods.append(config["stages"][stage]["type"])
            if "next" in config["stages"][stage]:
                name = config["stages"][stage]["next"]
                intel = config["stages"][name]
                config["stages"][stage]["next"] ="/"+intel["type"]+"/"+ name

    utils.config = config

    with open(utils.NAME_REP_CONFIG+'/data.json') as instance_data:
        instance_data = json.load(instance_data)

    utils.instance_data = instance_data

    utils.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+utils.NAME_REP_CONFIG+"/bdd_sqlite.db"
    utils.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    utils.app.secret_key = b'_5#y2zcer88L"Fczerzce4Q8sdqsdcezqtz\n\xec]/'
    utils.db = SQLAlchemy(utils.app)

    utils.app.url_map.converters['list'] = utils.ListConverter
    utils.app.register_blueprint(sstatic.bp,url_prefix='/static') # Register Blueprint

    if "auth_login" in active_mods:
        import mods.auth_login as ml
        from mods.auth_login.model import *
        utils.app.register_blueprint(ml.bp,url_prefix='/auth_login') # Register Blueprint
        safe_copy_rep(utils.ROOT+"/mods/auth_login/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/auth_login")

    if "pages" in active_mods:
        import mods.pages as mp
        utils.app.register_blueprint(mp.bp,url_prefix='/pages') # Register Blueprint
        safe_copy_rep(utils.ROOT+"/mods/pages/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/pages")

    if "questionnaire" in active_mods:
        import mods.questionnaire as mq
        utils.app.register_blueprint(mq.bp,url_prefix='/questionnaire') # Register Blueprint
        safe_copy_rep(utils.ROOT+"/mods/questionnaire/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/questionnaire")

    if "tests" in active_mods:
        import mods.tests as mt
        utils.app.register_blueprint(mt.bp,url_prefix='/tests') # Register Blueprint
        safe_copy_rep(utils.ROOT+"/mods/tests/templates",utils.NAME_REP_CONFIG+"/.tmp/templates/tests")

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
