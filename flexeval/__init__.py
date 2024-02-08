# coding: utf8
# license : CeCILL-C

# Python
import os
import random
import string
import datetime
import logging

# Flask
from flask import Flask

# FlexEval
from .utils import safe_make_rep
from .core import Config, ErrorHandler
from .core.providers import TemplateProvider, AssetsProvider
from .database import db
from .extensions import session_manager


def create_app(INSTANCE_PATH, INSTANCE_URL, debug=False, log_level=logging.INFO):
    """Application-factory pattern"""

    # Create Flask application
    app = Flask(__name__, template_folder=None, static_url_path=None)

    # Set logging level
    log = logging.getLogger("werkzeug")
    log.setLevel(log_level)

    # Config FLEXEVAL
    app.config.setdefault("FLEXEVAL_DIR", os.path.dirname(os.path.abspath(__file__)))
    app.config.setdefault("FLEXEVAL_INSTANCE_DIR", INSTANCE_PATH)
    app.config.setdefault("FLEXEVAL_INSTANCE_URL", INSTANCE_URL)
    app.config.setdefault("FLEXEVAL_INSTANCE_TMP_DIR", safe_make_rep(INSTANCE_PATH + "/.tmp"))

    # Config Session
    app.config.setdefault("SESSION_TYPE", "filesystem")
    app.config.setdefault("PERMANENT_SESSION_LIFETIME", datetime.timedelta(days=31))
    app.config.setdefault(
        "SECRET_KEY", "".join((random.choice(string.ascii_lowercase) for _ in range(20))).encode("ascii")
    )
    app.config.setdefault("SESSION_FILE_DIR", safe_make_rep(INSTANCE_PATH + "/.tmp/.sessions"))

    # Config SqlAlchemy
    app.config.setdefault("SQLALCHEMY_FILE", INSTANCE_PATH + "/flexeval.db")
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///" + app.config["SQLALCHEMY_FILE"])
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Initialisation of the DB connection
    db.init_app(app)

    # Session manager initialisation
    session_manager.init_app(app)

    # Init
    with app.app_context():
        # Instantiating the default providers
        AssetsProvider("/assets")
        TemplateProvider(app.config["FLEXEVAL_INSTANCE_TMP_DIR"] + "/templates")

        # Config app based on structure.json
        Config()

        # Module loaded => create the database
        db.create_all()

        # Error management
        ErrorHandler()

    return app
