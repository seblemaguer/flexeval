import random
from flask import session

class AuthProvider():

    def get(self):
        raise NotImplementedError()

    def set(self,*args):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()

class AnonAuthProvider(AuthProvider):

    def get(self):

        if "anon" in session:
            return session["anon"]
        else:
            self.set()
            return session["anon"]

    def set(self):
        session["anon"] = "anon@"+str(random.randint(1,999999999999999))

    def destroy(self):
        del session["anon"]
