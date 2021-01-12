# coding: utf8
# license : CeCILL-C

# Global
import os
import shutil
import sys

# Flask related
from flask import current_app
from flask import redirect as flask_redirect

def copytree(src, dst, dirs_exist_ok=True, ignore=None):
    """Alternative copytree to the shutils.copytree which is only available in python >= 3.8

    Parameters
    ----------
    src: file
        the source directory
    dst: file
        The target directory
    dirs_exist_ok: Boolean
        Always TRUE, else ignored!

    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, dirs_exist_ok=dirs_exist_ok, ignore=ignore)
        else:
            from pathlib import Path
            os.makedirs(Path(d).parent, exist_ok=dirs_exist_ok)
            shutil.copyfile(s, d)


def safe_make_rep(REP):
    """Make a fresh empty directory

    Parameters
    ----------
    REP: file
        The directory to (re)-create

    Returns
    -------
    File -> the directory path
    """

    if os.path.exists(REP):
        shutil.rmtree(REP)

    os.makedirs(REP)

    return REP


def create_file(FILE):
    """Create an empty file

    Parameters
    ----------
    FILE: file
        The file to create
    """

    with open(FILE, "w"):
        pass


def del_file(FILE):
    """Delete a file but don't crash if the file doesn't exist

    Parameters
    ----------
    FILE: file
        The file to delete
    """

    if os.path.isfile(FILE):
        os.remove(FILE)


def make_global_url(local_url):
    """Generate global URL from a local URL

    Parameters
    ----------
    local_url: string
        The local (relative) URL

    Returns
    -------
    string => the global (complete) URL
    """

    return current_app.config["FLEXEVAL_INSTANCE_URL"] + local_url


def redirect(local_url):
    """Prepare redirection to the local URL

    Parameters
    ----------
    local_url: string
        The local (relative) URL

    Returns
    -------
    Response object => which if called redirects the client to the target location
    """
    return flask_redirect(make_global_url(local_url))


class AppSingleton(type):
    def __call__(cls, *args, **kwargs):

        if not (hasattr(current_app, "_appsingleton_instances")):
            current_app._appsingleton_instances = {}

        if cls not in current_app._appsingleton_instances:
            current_app._appsingleton_instances[cls] = super(
                AppSingleton, cls
            ).__call__(*args, **kwargs)

        return current_app._appsingleton_instances[cls]
