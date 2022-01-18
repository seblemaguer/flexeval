# coding: utf8
# license : CeCILL-C

import random

from .AuthProvider import AuthProvider, UserModel


class AnonUser(UserModel):
    pass


class AnonAuthProvider(AuthProvider):

    __userBase__ = AnonUser

    def connect(self):
        super().connect(
            self.userModel.create(
                id="anon@" + str(random.randint(1, 999999999999999))
            )
        )

    def validates_connection(self, condition=None):
        if not (super().validates_connection("connected")[0]):
            self.connect()

        return super().validates_connection(condition)


    def disconnect(self):
        pass
