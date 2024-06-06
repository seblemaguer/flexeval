# Python
import pathlib
import random
import string
import datetime
import argparse

# Messaging/logging
import logging
from logging.config import dictConfig

# Flask
from flask import Flask
from werkzeug.serving import run_simple

# FlexEval
from flexeval.utils import safe_make_dir
from flexeval.core import error, campaign_instance
from flexeval.core import Config
from flexeval.core.providers import TemplateProvider, AssetsProvider, provider_factory
from flexeval.database import db
from flexeval.extensions import session_manager

###############################################################################
# global constants
###############################################################################
LEVEL: list[int] = [logging.WARNING, logging.INFO, logging.DEBUG]
INSTANCE_CONFIGURATION_BASENAME: str = "structure.yaml"


###############################################################################
# Functions
###############################################################################
def configure_logger(args) -> tuple[logging.Logger, int]:
    """Setup the global logging configurations and instanciate a specific logger for the current script

    Parameters
    ----------
    args : dict
        The arguments given to the script

    Returns
    --------
    the logger: logger.Logger
    """
    # create logger and formatter
    logger = logging.getLogger()

    # Verbose level => logging level
    log_level: int = int(args.verbosity)
    if log_level >= len(LEVEL):
        log_level = len(LEVEL) - 1
        # logging.warning("verbosity level is too high, I'm gonna assume you're taking the highest (%d)" % log_level)

    # Define the default logger configuration
    logging_config = dict(
        version=1,
        disable_existing_logger=True,
        formatters={
            "f": {
                "format": "[%(asctime)s] [%(levelname)s] — [%(name)s — %(funcName)s:%(lineno)d] %(message)s",
                "datefmt": "%d/%b/%Y: %H:%M:%S ",
            }
        },
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": LEVEL[log_level],
            }
        },
        root={"handlers": ["h"], "level": LEVEL[log_level]},
    )

    # Add file handler if file logging required
    if args.log_file is not None:
        logging_config["handlers"]["f"] = {
            "class": "logging.FileHandler",
            "formatter": "f",
            "level": LEVEL[log_level],
            "filename": args.log_file,
        }
        logging_config["root"]["handlers"] = ["h", "f"]

    # Setup logging configuration
    dictConfig(logging_config)

    # Retrieve and return the logger dedicated to the script
    logger = logging.getLogger(__name__)
    return logger, log_level


def define_argument_parser() -> argparse.ArgumentParser:
    """Defines the argument parser

    Returns
    --------
    The argument parser: argparse.ArgumentParser
    """

    # On récup les args liés à l'instance a créer
    parser = argparse.ArgumentParser(description="FlexEval")
    parser.add_argument("instance_entryfile", metavar="INSTANCE_DIRECTORY", type=str, help="Instance's directory")

    # Connection options
    parser.add_argument("-d", "--debug", action="store_true", help="Start the server in debugging mode")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="IP's server")
    parser.add_argument("-p", "--port", type=int, default="8080", help="port")
    parser.add_argument("-P", "--production", action="store_true", help="Start the server in production mode")
    parser.add_argument("-t", "--threaded", action="store_true", default=False, help="Enable threads.")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of the server (needed for flask redirections!) if different from http://<ip>:<port>/",
    )

    # Logging options
    parser.add_argument("-l", "--log_file", default=None, help="Logger file")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")

    # Return parser
    return parser


def create_app(
    instance_entrypoint: pathlib.Path, instance_url: str, debug: bool = False, log_level: int = logging.INFO
) -> Flask:
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

    instance_dir: pathlib.Path = instance_entrypoint.parent.resolve()

    # Create Flask application
    app: Flask = Flask(__name__, template_folder="", static_url_path=None)

    # Set logging level
    log = logging.getLogger("werkzeug")
    log.setLevel(log_level)

    # Config FLEXEVAL
    app.config.setdefault("FLEXEVAL_DIR", str(pathlib.Path(__file__).parent))
    app.config.setdefault("FLEXEVAL_INSTANCE_DIR", str(instance_dir))
    app.config.setdefault("FLEXEVAL_INSTANCE_URL", instance_url)
    app.config.setdefault("FLEXEVAL_INSTANCE_TMP_DIR", safe_make_dir(str(instance_dir / ".tmp")))

    # Config Session
    app.config.setdefault("SESSION_TYPE", "filesystem")
    app.config.setdefault("PERMANENT_SESSION_LIFETIME", datetime.timedelta(days=31))
    app.config.setdefault(
        "SECRET_KEY", "".join((random.choice(string.ascii_lowercase) for _ in range(20))).encode("ascii")
    )
    app.config.setdefault("SESSION_FILE_DIR", safe_make_dir(str(instance_dir / ".tmp/.sessions")))

    # Config SqlAlchemy
    app.config.setdefault("SQLALCHEMY_FILE", str(instance_dir / "flexeval.db"))
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
        config = Config(instance_entrypoint)
        campaign_instance.load_config(config)

        # Module loaded => create the database
        db.create_all()

        # Error management
        error.error_handler = error.ErrorHandler(app, config)  # type: ignore

    return app


def main():

    # Initialization
    arg_parser = define_argument_parser()
    args = arg_parser.parse_args()
    logger, log_level = configure_logger(args)

    # Get the instance absolute path
    instance_entrypoint: pathlib.Path = pathlib.Path(args.instance_entryfile)

    # List all the instance files to listen
    all_files: list[pathlib.Path] = list(instance_entrypoint.parent.glob("**/*"))
    extra_files: list[str] = []
    for f in all_files:
        if (str(f).find("/.tmp/") == -1) and (str(f).find("/assets/tmp_eval/") == -1) and (not str(f).endswith(".db")):
            extra_files.append(str(f))

    # Finally create and run app
    if args.url:
        app = create_app(instance_entrypoint, args.url, debug=args.debug, log_level=log_level)
    else:
        app = create_app(
            instance_entrypoint, "http://%s:%d" % (args.ip, args.port), debug=args.debug, log_level=log_level
        )

    if args.debug:
        app.run(
            host=args.ip,
            port=args.port,
            use_reloader=False,
            debug=args.debug,
            extra_files=extra_files,
            threaded=args.threaded,
        )
    elif not args.production:
        run_simple(hostname=args.ip, port=args.port, application=app, threaded=args.threaded, use_reloader=True)
    else:

        from gunicorn.app.base import BaseApplication

        class GunicornApp(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            "bind": [f"{args.ip}:{args.port}"],
            "worker_class": "gevent",
        }
        gunicorn_app = GunicornApp(app, options)
        gunicorn_app.run()
