# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import AuthProvider

class AdminUser():

    @property
    def id(self):
        return "admin"

class UniqueAuth(AuthProvider):

    __userBase__ = None

    def connect(self):
        super().connect(AdminUser())
