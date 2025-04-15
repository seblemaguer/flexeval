# coding: utf8
# license : CeCILL-C

from flexeval.core.stage import StageModuleUser
from flexeval.database import Column, db


class ProlificUser(StageModuleUser):
    study_id = Column(db.String, default="")
    session_id = Column(db.String, default="")

    def __init__(self, user_id: str, study_id: str, session_id: str):
        super().__init__()

        self.id = user_id

        # Get other fields
        self.study_id = study_id
        self.session_id = session_id
