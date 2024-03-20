# Python
from flexeval.core.providers.auth import AuthProvider, UserModel
from flexeval.mods.direct_auth.model import EmailUser, ProlificUser


class EmailAuth(AuthProvider):
    __userBase__ = EmailUser

    def connect(self, email: str):  # type: ignore
        user: UserModel | None = self.user_model.query.filter(self.user_model.id == email).first()  # type: ignore

        if user is None:
            user = self.user_model.create(email=email)  # type: ignore

        super().connect(user)  # type: ignore


class ProlificAuth(AuthProvider):
    __userBase__ = ProlificUser

    def __init__(self, name: str, local_url_homepage: str):
        super().__init__(name, local_url_homepage, ProlificUser)

    def connect(self, user_id, study_id, session_id):
        user = self.user_model.query.filter(self.user_model.id == user_id).first()

        if user is None:
            user = self.user_model.create(user_id=user_id, study_id=study_id, session_id=session_id)

        super().connect(user)
