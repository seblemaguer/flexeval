# Import Libraries
import os
import shutil

from core.src.providers import AuthProvider

NAME_REP_CONFIG = None
ROOT = None

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
