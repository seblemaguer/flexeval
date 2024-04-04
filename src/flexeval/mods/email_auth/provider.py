# Python
from flexeval.core.providers.auth import AuthProvider, UserModel
from .model import EmailUser


class EmailAuth(AuthProvider):
    __userBase__ = EmailUser

    def connect(self, email: str):  # type: ignore
        user: UserModel | None = self.user_model.query.filter(self.user_model.id == email).first()

        if user is None:
            user = self.user_model.create(email=email)

        super().connect(user)
