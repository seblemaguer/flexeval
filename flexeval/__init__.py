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
from .utils import safe_make_dir
from .core import Config, error
from .core.providers import TemplateProvider, AssetsProvider, provider_factory
from .database import db
from .extensions import session_manager


def create_app(instance_path: str, instance_url: str, debug: bool = False, log_level: int = logging.INFO) -> Flask:
    """Create the Flask Application

    Parameters
    ----------
    instance_path : str
        The path of the instance to run
    instance_url : str
        The URL of the instance to run
    debug : bool
        Shall we activate the debug mode?
    log_level : int
        the default logging level

    Returns
    -------
    Flask
        The created Flask application associated to the instance
    """

    # Create Flask application
    app: Flask = Flask(__name__, template_folder="", static_url_path=None)

    # Set logging level
    log = logging.getLogger("werkzeug")
    log.setLevel(log_level)

    # Config FLEXEVAL
    app.config.setdefault("FLEXEVAL_DIR", os.path.dirname(os.path.abspath(__file__)))
    app.config.setdefault("FLEXEVAL_INSTANCE_DIR", instance_path)
    app.config.setdefault("FLEXEVAL_INSTANCE_URL", instance_url)
    app.config.setdefault("FLEXEVAL_INSTANCE_TMP_DIR", safe_make_dir(instance_path + "/.tmp"))

    # Config Session
    app.config.setdefault("SESSION_TYPE", "filesystem")
    app.config.setdefault("PERMANENT_SESSION_LIFETIME", datetime.timedelta(days=31))
    app.config.setdefault(
        "SECRET_KEY", "".join((random.choice(string.ascii_lowercase) for _ in range(20))).encode("ascii")
    )
    app.config.setdefault("SESSION_FILE_DIR", safe_make_dir(instance_path + "/.tmp/.sessions"))

    # Config SqlAlchemy
    app.config.setdefault("SQLALCHEMY_FILE", instance_path + "/flexeval.db")
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///" + app.config["SQLALCHEMY_FILE"])
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Initialisation of the DB connection
    db.init_app(app)

    # Session manager initialisation
    session_manager.init_app(app)

    # Init
    with app.app_context():
        # Instantiating the default providers
        provider_factory.set(AssetsProvider.NAME, AssetsProvider("/assets"))
        provider_factory.set(
            TemplateProvider.NAME, TemplateProvider(app.config["FLEXEVAL_INSTANCE_TMP_DIR"] + "/templates")
        )

        # Config app based on structure.json
        _ = Config()

        # Module loaded => create the database
        db.create_all()

        # Error management
        error.error_handler = error.ErrorHandler(app)

    return app
