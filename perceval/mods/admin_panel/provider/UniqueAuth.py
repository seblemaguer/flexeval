# coding: utf8
from perceval.core import AuthProvider

class AdminUser():

    @property
    def pseudo(self):
        return "admin"

class UniqueAuth(AuthProvider):

    __userBase__ = None

    def connect(self):
        super().connect(AdminUser())
