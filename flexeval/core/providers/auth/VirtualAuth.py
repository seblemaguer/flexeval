# coding: utf8
# license : CeCILL-C

from .AuthProvider import AuthProvider


class NotConnectedError(Exception):
    pass


class VirtualAuthProvider(AuthProvider):

    __userBase__ = None

    def __init__(self, name=None, local_url_homepage=None, userModel=None):
        if name == None:
            pass
        else:
            super(VirtualAuthProvider, self).__init__(
                name, local_url_homepage, userModel
            )

    def connect(self, *args):
        raise NotConnectedError()

    def validates_connection(self, condition=None):
        return (False, "connected")
