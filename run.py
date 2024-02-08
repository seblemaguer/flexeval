#!/usr/bin/env python3
# coding: utf8
# license : CeCILL-C

# Python
from typing import Tuple

# Arguments
import argparse

# Messaging/logging
import logging
from logging.config import dictConfig

# Globbing
import glob
import os

# FlexEval entry points
from werkzeug.serving import run_simple
from flexeval import create_app

###############################################################################
# global constants
###############################################################################
LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]


###############################################################################
# Functions
###############################################################################
def configure_logger(args) -> Tuple[logging.Logger, int]:
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
    parser.add_argument("instance", metavar="INSTANCE_DIRECTORY", type=str, help="Instance's directory")

    # Connection options
    parser.add_argument("-d", "--debug", action="store_true", help="Start the server in debugging mode")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="IP's server")
    parser.add_argument("-p", "--port", type=int, default="8080", help="port")
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


###############################################################################
#  Envelopping
###############################################################################
if __name__ == "__main__":
    # Initialization
    arg_parser = define_argument_parser()
    args = arg_parser.parse_args()
    logger, log_level = configure_logger(args)

    # Get the instance absolute path
    instance_abs_path = os.path.abspath(args.instance)

    # List all the instance files to listen
    all_files = glob.glob(instance_abs_path + "/**/*", recursive=True)
    extra_files = []
    for f in all_files:
        if (f.find("/.tmp/") == -1) and (f.find("/assets/tmp_eval/") == -1) and (not f.endswith(".db")):
            extra_files.append(f)

    # Finally create and run app
    if args.url:
        app = create_app(instance_abs_path, args.url, debug=args.debug, log_level=log_level)
    else:
        app = create_app(
            instance_abs_path, "http://%s:%d" % (args.ip, args.port), debug=args.debug, log_level=log_level
        )

    if args.debug:
        app.run(
            host=args.ip,
            port=args.port,
            use_reloader=True,
            debug=args.debug,
            extra_files=extra_files,
            threaded=args.threaded,
        )
    else:
        run_simple(hostname=args.ip, port=args.port, application=app, threaded=args.threaded, use_reloader=True)
