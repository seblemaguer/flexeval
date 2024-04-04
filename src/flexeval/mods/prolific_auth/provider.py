# Python
from flexeval.core.providers.auth import AuthProvider
from .model import ProlificUser


class ProlificAuth(AuthProvider):
    __userBase__ = ProlificUser

    def connect(self, user_id: str, study_id: str, session_id: str):
        user = self.user_model.query.filter(self.user_model.id == user_id).first()

        if user is None:
            user = self.user_model.create(user_id=user_id, study_id=study_id, session_id=session_id)

        super().connect(user)
