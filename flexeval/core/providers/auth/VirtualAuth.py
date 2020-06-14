# coding: utf8
# license : CeCILL-C

from flexeval.core import AuthProvider

class NotConnectedError(Exception):
    pass

class VirtualAuthProvider(AuthProvider):

    __userBase__ = None

    def __init__(self,name=None,local_url_homepage=None,userModel=None):
        if name == None:
            pass
        else:
            super().__init__(name,local_url_homepage,userModel)

    def connect(self,*args):
        raise NotConnectedError()

    @property
    def is_connected(self):
        return False
