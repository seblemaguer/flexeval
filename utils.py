from src.providers import AuthProvider
from werkzeug.routing import BaseConverter

#https://readthedocs.org/projects/pallet/downloads/pdf/latest/
class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return','.join(super(ListConverter, self).to_url(value) for value in values)


NAME_REP_CONFIG = None
ROOT = None

app = None
db = None
instance_data = None

providers = {"auth":AuthProvider.AnonAuthProvider()}

def set_provider(key,prov):
    providers[key] = prov

def get_provider(key):
    return providers[key]
