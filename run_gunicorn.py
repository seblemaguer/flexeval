#!/usr/bin/env python3

# Python
import pathlib
import argparse

# Messaging/logging
import logging
from logging.config import dictConfig

# Globbing
import glob

# FlexEval entry points
from gunicorn.app.base import BaseApplication
from flexeval import create_app

###############################################################################
# global constants
###############################################################################
LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]


###############################################################################
# Helper classes
##############################################################################
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
    log_level = args.verbosity
    if args.verbosity >= len(LEVEL):
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
    _ = parser.add_argument("instance_entryfile", metavar="INSTANCE_DIRECTORY", type=str, help="Instance's directory")

    # Connection options
    _ = parser.add_argument("-d", "--debug", action="store_true", help="Start the server in debugging mode")
    _ = parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="IP's server")
    _ = parser.add_argument("-p", "--port", type=int, default="8080", help="port")
    _ = parser.add_argument("-t", "--threaded", action="store_true", default=False, help="Enable threads.")
    _ = parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of the server (needed for flask redirections!) if different from http://<ip>:<port>/",
    )

    # Logging options
    _ = parser.add_argument("-l", "--log_file", default=None, help="Logger file")
    _ = parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")

    # Return parser
    return parser


###############################################################################
#  Envelopping
###############################################################################
if __name__ == "__main__":
    # Initialization
    arg_parser = define_argument_parser()
    args = arg_parser.parse_args()
    logger, log_level = configure_logger(args)

    # Get the instance absolute path
    instance_entrypoint: pathlib.Path = pathlib.Path(args.instance_entryfile)
    instance_dir: pathlib.Path = instance_entrypoint.parent.resolve()

    # List all the instance files to listen
    all_files: list[str] = glob.glob(str(instance_dir / "**/*"), recursive=True)
    extra_files: list[str] = []
    for f in all_files:
        if (f.find("/.tmp/") == -1) and (f.find("/assets/tmp_eval/") == -1) and (not f.endswith(".db")):
            extra_files.append(f)

    # Finally create and run app
    if args.url:
        app = create_app(instance_entrypoint, args.url, debug=args.debug, log_level=log_level)
    else:
        app = create_app(
            instance_entrypoint, "http://%s:%d" % (args.ip, args.port), debug=args.debug, log_level=log_level
        )

    options = {
        "bind": [f"{args.ip}:{args.port}"],
        "worker_class": "gevent",
    }
    gunicorn_app = GunicornApp(app, options)
    gunicorn_app.run()
