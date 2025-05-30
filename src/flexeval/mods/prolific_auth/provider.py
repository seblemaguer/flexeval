# Python
from flexeval.core.providers.auth import AuthProvider
from .model import ProlificUser


class ProlificAuthProvider(AuthProvider):
    __userBase__ = ProlificUser

    def connect(self, user_id: str, study_id: str, session_id: str) -> None:
        assert self.user_model is not None
        user: ProlificUser | None = ProlificUser.query.filter(self.user_model.user_id == user_id).first()

        if user is None:
            user = ProlificUser.create(user_id=user_id, study_id=study_id, session_id=session_id)

        super()._connect(user)
