# coding: utf8
# license : CeCILL-C

import os
import random
import string
import datetime

from flask import Flask, current_app, g

import sqlalchemy

from .utils import safe_copy_rep,safe_make_rep, del_file, create_file
from .core import Config, Provider, ErrorHandler
from .core.providers import assets, templates

from .extensions import db,session_manager

def create_app(INSTANCE_PATH,INSTANCE_URL):
    """Application-factory pattern"""

    app = Flask(__name__,template_folder = None,static_url_path=None)

    # Config FLEXEVAL
    app.config.setdefault("FLEXEVAL_DIR",os.path.dirname(os.path.abspath(__file__)))
    app.config.setdefault("FLEXEVAL_INSTANCE_DIR",INSTANCE_PATH)
    app.config.setdefault("FLEXEVAL_INSTANCE_URL",INSTANCE_URL)
    app.config.setdefault("FLEXEVAL_INSTANCE_TMP_DIR",safe_make_rep(INSTANCE_PATH+"/.tmp"))

    # Config Session
    app.config.setdefault("SESSION_TYPE","filesystem")
    app.config.setdefault('PERMANENT_SESSION_LIFETIME',datetime.timedelta(days=31))
    app.config.setdefault('SECRET_KEY',''.join((random.choice(string.ascii_lowercase) for i in range(20))).encode('ascii'))
    app.config.setdefault('SESSION_FILE_DIR',safe_make_rep(INSTANCE_PATH+"/.tmp/.sessions"))

    # Config SqlAlchemy
    app.config.setdefault('SQLALCHEMY_FILE',INSTANCE_PATH+"/flexeval.db")
    app.config.setdefault('SQLALCHEMY_DATABASE_URI',"sqlite:///"+app.config["SQLALCHEMY_FILE"])
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS',False)

    # On intialise la co à la db
    db.init_app(app)

    # On initialise session manager
    session_manager.init_app(app)

    # Init
    with app.app_context():

        # On instancie les providers par défault
        assets.default("/assets")
        templates.default(app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/templates")

        # Config app based on structure.json
        Config()

        # Tous les modules ont été chargés donc on peut gen la db
        db.create_all()

        # Gestion des erreurs
        ErrorHandler()

    return app
