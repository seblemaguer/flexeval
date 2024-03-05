# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import AuthProvider
from flexeval.mods.direct_auth.model import EmailUser, ProlificUser


class EmailAuth(AuthProvider):
    __userBase__ = EmailUser

    def connect(self, email):
        user = self.userModel.query.filter(self.userModel.id == email).first()

        if user is None:
            user = self.userModel.create(email=email)

        super().connect(user)


class ProlificAuth(AuthProvider):
    __userBase__ = ProlificUser

    def connect(self, user_id, study_id, session_id):
        user = self.userModel.query.filter(self.userModel.id == user_id).first()

        if user is None:
            user = self.userModel.create(user_id=user_id, study_id=study_id, session_id=session_id)

        super().connect(user)
