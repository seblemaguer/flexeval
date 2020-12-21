# coding: utf8
# license : CeCILL-C

import argparse
import os

# Logging part
import logging

# Globbing
import glob

# FlexEval entry points
from flexeval import create_app

LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]

if __name__ == "__main__":

    # On récup les args liés à l'instance a créer
    parser = argparse.ArgumentParser(description="FlexEval")
    parser.add_argument(
        "instance", metavar="INSTANCE_DIRECTORY", type=str, help="Instance's directory"
    )

    # Connection options
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Start the server in debugging mode"
    )
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="IP's server")
    parser.add_argument("-p", "--port", type=int, default="8080", help="port")

    # Logging options
    parser.add_argument(
        "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
    )

    args = parser.parse_args()

    # create logger and formatter
    logger = logging.getLogger()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Verbose level => logging level
    log_level = args.verbosity
    if args.verbosity >= len(LEVEL):
        log_level = len(LEVEL) - 1
        logger.setLevel(log_level)
        logging.warning(
            "verbosity level is too high, I'm gonna assume you're taking the highest (%d)"
            % log_level
        )
    else:
        logger.setLevel(LEVEL[log_level])

    # create console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Get the instance absolute path
    instance_abs_path = os.path.abspath(args.instance)

    # List all the instance files to listen
    all_files = glob.glob(instance_abs_path + "/**/*", recursive=True)
    extra_files = []
    for f in all_files:
        if (f.find("/.tmp/") == -1) and (not f.endswith(".db")):
            extra_files.append(f)

    # Finally create and run app
    app = create_app(instance_abs_path, "http://%s:%d" % (args.ip, args.port), debug=args.debug)

    log = logging.getLogger('werkzeug')
    log.setLevel(log_level)

    app.run(
        host=args.ip,
        port=args.port,
        use_reloader=True,
        debug=args.debug,
        extra_files=extra_files,
    )
