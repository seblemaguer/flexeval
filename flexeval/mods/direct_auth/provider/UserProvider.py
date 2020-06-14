# coding: utf8
# license : CeCILL-C

import random

from flexeval.core import AuthProvider
from flexeval.mods.direct_auth.model import EmailUser

class EmailAuth(AuthProvider):

    __userBase__ = EmailUser

    def connect(self,email):
        user = self.userModel.query.filter(self.userModel.pseudo == email).first()

        if user is None:
            user = self.userModel.create(email=email)

        super().connect(user)
