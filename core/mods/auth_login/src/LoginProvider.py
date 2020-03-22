# Import Libraries
from flask import session, abort

from core.src.providers.AuthProvider import AuthProvider

class LoginAuthProvider(AuthProvider):

    def get(self):

        if self.connected:
            return session["user"]
        else:
            abort(401)

    def set(self,user):
        session["user"] = user

    def destroy(self):
        del session["user"]

    @property
    def connected(self):
        return "user" in session
