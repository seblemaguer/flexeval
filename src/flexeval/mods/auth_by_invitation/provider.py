# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import AuthProvider
from .model import InvitedUser


class UserAuthError(Exception):
    pass


class BadCredential(UserAuthError):
    pass


class UserAuth(AuthProvider):
    __userBase__ = InvitedUser

    def connect(self, token):
        assert self.user_model is not None
        assert isinstance(self.user_model, InvitedUser)
        user: InvitedUser | None = InvitedUser.query.filter(self.user_model.token == token).first()

        if user is None:
            raise BadCredential()
        else:
            super()._connect(user)
