# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import UserModel
from flexeval.database import Column, db

import re


class NotAnEmail(Exception):
    def __init__(self, email):
        self.email = email


EMAIL_REGEX = re.compile(r"^([\w\.\-]+)@([\w\-]+)((\.([\w-]){2,63}){1,3})$")


class EmailUser(UserModel):
    def __init__(self, email):
        # Validate email
        if not re.fullmatch(EMAIL_REGEX, email):
            raise NotAnEmail(email)

        # Set the email as the ID
        self.id = email


class ProlificUser(UserModel):
    study_id = Column(db.String, default="")
    session_id = Column(db.String, default="")

    def __init__(self, email, study_id, session_id):
        # Validate email
        if not re.fullmatch(EMAIL_REGEX, email):
            raise NotAnEmail(email)

        # Set the email as the ID
        self.id = email

        # Get other fields
        self.study_id = study_id
        self.session_id = session_id
