import random

from perceval.core import AuthProvider
from perceval.mods.direct_auth.model import EmailUser

class EmailAuth(AuthProvider):

    __userBase__ = EmailUser

    def connect(self,email):
        user = self.userModel.query.filter(self.userModel.pseudo == email).first()

        if user is None:
            user = self.userModel.create(email=email)

        super().connect(user)
