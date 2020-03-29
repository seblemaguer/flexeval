# Import Libraries
import random

from flask import session, abort

class AuthProvider():

    def get(self):
        raise NotImplementedError()

    def set(self,*args):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()

    @property
    def connected(self):
        raise NotImplementedError()

class AnonAuthProvider(AuthProvider):

    def get(self):
        if self.connected:
            return session["user"]
        else:
            self.set()
            return session["user"]

    def set(self):
        session["anon"] = "anon@"+str(random.randint(1,999999999999999))
        session.permanent = True

    def destroy(self):
        pass

    @property
    def connected(self):
        return "user" in session

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
