# coding: utf8
# license : CeCILL-C

from flexeval.core import AuthProvider

class AdminUser():

    @property
    def pseudo(self):
        return "admin"

class UniqueAuth(AuthProvider):

    __userBase__ = None

    def connect(self):
        super().connect(AdminUser())
