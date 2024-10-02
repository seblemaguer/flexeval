# Python
from flexeval.core.providers.auth import AuthProvider
from .model import EmailUser


class EmailAuthProvider(AuthProvider):
    __userBase__ = EmailUser

    def connect(self, email: str):  # type: ignore
        assert self.user_model is not None
        user: EmailUser | None = EmailUser.query.filter(self.user_model.id == email).first()

        if user is None:
            user = EmailUser.create(email=email)

        super()._connect(user)
