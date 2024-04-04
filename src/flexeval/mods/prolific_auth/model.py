# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import UserModel
from flexeval.database import Column, db


class ProlificUser(UserModel):
    study_id = Column(db.String, default="")
    session_id = Column(db.String, default="")

    def __init__(self, user_id: str, study_id: str, session_id: str):
        super().__init__()
        # Set the email as the ID
        self.id = user_id

        # Get other fields
        self.study_id = study_id
        self.session_id = session_id
