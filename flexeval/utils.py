# coding: utf8
# license : CeCILL-C

import os
import shutil

from flask import current_app
from flask import redirect as flask_redirect

def safe_copy_rep(SRC,DST):

    if not os.path.exists(DST):
        os.makedirs(DST)

    if os.path.exists(SRC):

        DST_files = os.listdir(DST)
        SRC_files = os.listdir(SRC)

        for file in SRC_files:
            if not(file in DST_files):
                if(os.path.isdir(SRC+"/"+file)):
                    safe_copy_rep(SRC+"/"+file,DST+"/"+file)
                else:
                    shutil.copyfile(SRC+"/"+file,DST+"/"+file)

def safe_make_rep(REP):
    if os.path.exists(REP):
        shutil.rmtree(REP)

    os.makedirs(REP)

    return REP

def create_file(FILE):
    with open(FILE, "w"):
        pass

def del_file(FILE):
    if os.path.isfile(FILE):
        os.remove(FILE)

def make_global_url(local_url):
    return current_app.config["FLEXEVAL_INSTANCE_URL"] + local_url

def redirect(local_url):
    return flask_redirect(make_global_url(local_url))

class AppSingleton(type):

    def __call__(cls, *args, **kwargs):

        if(not(hasattr(current_app,"_appsingleton_instances"))):
            current_app._appsingleton_instances = {}

        if cls not in current_app._appsingleton_instances:
            current_app._appsingleton_instances[cls] = super(AppSingleton, cls).__call__(*args, **kwargs)

        return current_app._appsingleton_instances[cls]
