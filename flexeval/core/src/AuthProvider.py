# coding: utf8
# license : CeCILL-C

from flask import session as flask_session
from flask import current_app, redirect

from .Provider import Provider,UndefinedError

from flexeval.utils import make_global_url,redirect
from flexeval.database import Model,Column, db

class AuthProviderError(Exception):
    pass

class UserBase():
    pseudo = Column(db.String, primary_key=True)

    def allow(self,role=None):
        return True

class AuthProvider():

    def __init__(self,name,local_url_homepage,userModel):
        self.local_url_homepage = local_url_homepage
        self.name = name
        self.userModel = userModel

        try:
            current_app.add_url_rule('/deco/<name>',"deco",self.__class__.disconnect_action)
        except AssertionError as e:
            pass

        print(" * AuthProvider:"+self.__class__.__name__+" named:"+name+" is loaded.")

        Provider().set(name,self)

    @classmethod
    def disconnect_action(cls,name):
        provider = Provider().get(name)

        try:
            provider.disconnect()
        except Exception as e:
            pass

        return redirect(provider.local_url_homepage)

    @property
    def user(self):
        if self.userModel.__abstract__:
            return self.session["user"]
        else:
            return self.userModel.query.filter(self.userModel.pseudo == self.session["user"]).first()

    def connect(self,user):
        if self.userModel.__abstract__:
            self.session["user"] = user
        else:
            self.session["user"] = user.pseudo

    def disconnect(self):
        del self.session["user"]

    @property
    def is_connected(self):
        return "user" in self.session

    @property
    def url_deco(self):
        return make_global_url('/deco/'+self.name)

    @property
    def session(self):
        if "authprovider:"+str(self.name) not in flask_session.keys():
            flask_session["authprovider:"+str(self.name)] = {}

        return flask_session["authprovider:"+str(self.name)]
