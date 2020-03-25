# Import Libraries
import random

from flask import session

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
            return session["anon"]
        else:
            self.set()
            return session["anon"]

    def set(self):
        session["anon"] = "anon@"+str(random.randint(1,999999999999999))
        session.permanent = True
        
    def destroy(self):
        pass

    @property
    def connected(self):
        return "anon" in session
