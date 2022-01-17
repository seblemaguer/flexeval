# coding: utf8
# license : CeCILL-C

from flexeval.core.providers.auth import UserModel


class NotAnEmail(Exception):
    def __init__(self, email):
        self.email = email


class EmailUser(UserModel):
    def __init__(self, email):

        try:
            split = email.split("@")
            assert len(split) == 2
            domain = split[1].split(".")
            assert len(domain) == 2
        except Exception as e:
            raise NotAnEmail(email)

        self.pseudo = email
