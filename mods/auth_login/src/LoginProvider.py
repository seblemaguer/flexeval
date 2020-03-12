from flask import session, redirect
from src.providers.AuthProvider import AuthProvider

class LoginAuthProvider(AuthProvider):

    def get(self):

        if "user" in session:
            return session["user"]
        else:
            return redirect("/auth_login/login")

    def set(self,userid):
        session["user"] = userid

    def destroy(self):
        del session["user"]
