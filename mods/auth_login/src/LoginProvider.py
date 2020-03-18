from flask import session, abort
from src.providers.AuthProvider import AuthProvider

class LoginAuthProvider(AuthProvider):

    def get(self):

        if "user" in session:
            return session["user"]
        else:
            abort(401)

    def set(self,userid):
        session["user"] = userid

    def destroy(self):
        del session["user"]
