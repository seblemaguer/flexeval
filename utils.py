from src.providers import AuthProvider
from flask import Blueprint,render_template

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
