import random

from flask import session

from perceval.core import AuthProvider, UserBase
from perceval.database import Model,Column,db

class AnonUser(UserBase):
    pass

class AnonAuthProvider(AuthProvider):

    __userBase__ = AnonUser

    def connect(self):
        super().connect(self.userModel.create(pseudo="anon@"+str(random.randint(1,999999999999999))))

    @property
    def is_connected(self):
        if not(super().is_connected):
            self.connect()

        return True

    def disconnect(self):
        pass
