# Import Libraries
from flask import Flask,redirect,session
from flask_sqlalchemy import SQLAlchemy
import json
import utils
import argparse
import os


#  Main
if __name__ == '__main__':

    # Arguments Parsing
    parser = argparse.ArgumentParser(description='PercEval')
    parser.add_argument("config",metavar='CONFIG_REP', type=str, help='configuration')
    args = parser.parse_args()

    utils.NAME_REP_CONFIG = os.path.dirname(os.path.abspath(__file__))+"./instances/"+args.config

    utils.app = Flask(__name__, instance_relative_config=False)
    with open(utils.NAME_REP_CONFIG+'/config.json') as config:
        utils.config = json.load(config)

    utils.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+utils.NAME_REP_CONFIG+"/"+utils.config["SQLALCHEMY_DATABASE_URI"]
    utils.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    utils.app.secret_key = b'_5#y2zcer88L"Fczerzce4Q8sdqsdcezqtz\n\xec]/'
    utils.db = SQLAlchemy(utils.app)

    if "auth" in utils.config["use"]:
        import mods.auth as ml
        from mods.auth.model import *
        utils.app.register_blueprint(ml.bp,url_prefix='/auth') # Register Blueprint

    if "pages" in utils.config["use"]:
        import mods.pages as mp
        utils.app.register_blueprint(mp.bp,url_prefix='/pages') # Register Blueprint

    if "questionnaire" in utils.config["use"]:
        import mods.questionnaire as mq
        utils.app.register_blueprint(mq.bp,url_prefix='/questionnaire') # Register Blueprint

    if "tests" in utils.config["use"]:
        import mods.tests as mt
        utils.app.register_blueprint(mt.bp,url_prefix='/tests') # Register Blueprint

    utils.db.create_all()


    @utils.app.route('/')
    def main_route():
        return redirect(utils.config["entrypoint"])

    # Run app
    utils.app.run(host=utils.config["HOST"],port=int(utils.config["PORT"]))
