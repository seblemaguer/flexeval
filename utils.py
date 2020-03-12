from src.providers import AuthProvider

NAME_REP_CONFIG = None

app = None
db = None
config = None

providers = {"auth":AuthProvider.AnonAuthProvider()}

def set_provider(key,prov):
    providers[key] = prov

def get_provider(key):
    return providers[key]
