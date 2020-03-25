# Import Libraries
import os
import shutil

from core.src.providers import AuthProvider
from flask import render_template as flask_render_template

NAME_REP_CONFIG = None
ROOT = None

jwt = None
app = None
db = None

providers = {"auth":AuthProvider.AnonAuthProvider()}
assets = None

def set_provider(key,prov):
    providers[key] = prov

def get_provider(key):
    return providers[key]

def safe_copy_rep(SRC,DST):

    if not os.path.exists(DST):
        os.makedirs(DST)

    if os.path.exists(SRC):

        DST_files = os.listdir(DST)
        SRC_files = os.listdir(SRC)

        for file in SRC_files:
            if not(file in DST_files):
                shutil.copyfile(SRC+"/"+file,DST+"/"+file)

def render_template(template,**args):

    args["next"] = config["entrypoint"]
    args["userprov"] = get_provider("auth")
    variables = {}

    if "variables" in config:
        variables = config["variables"]

    if "stage_name" in args:

        if "next" in config["stages"][args["stage_name"]]:
            args["next"] = config["stages"][args["stage_name"]]["next"]


        if "variables" in config["stages"][args["stage_name"]]:

            for _varkey in config["stages"][args["stage_name"]]["variables"].keys():
                variables[_varkey] = config["stages"][args["stage_name"]]["variables"][_varkey]

    def fvariables(key,default_value=""):
        if key in variables:
            return variables[key]
        else:
            return default_value

    args["variables"] = fvariables

    return flask_render_template(template,**args)
