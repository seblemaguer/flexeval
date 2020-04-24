# coding: utf8
# license : CeCILL-C

from flexeval.core import AuthProvider
from flexeval.mods.auth_by_invitation.model import User

class UserAuthError(Exception):
    pass

class BadCredential(UserAuthError):
    pass

class UserAuth(AuthProvider):

    __userBase__ = User

    def connect(self,token):
        user = self.userModel.query.filter(self.userModel.token == token).first()

        if user is None:
            raise BadCredential()
        else:
            super().connect(user)
