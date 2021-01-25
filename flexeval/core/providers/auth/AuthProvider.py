# coding: utf8
# license : CeCILL-C

import logging

import abc


from flask import session as flask_session
from flask import current_app, redirect

from flexeval.core import ProviderFactory, UndefinedError
from flexeval.utils import make_global_url, redirect
from flexeval.database import Model, Column, db


class AuthProviderError(Exception):
    pass


class UserBase:
    pseudo = Column(db.String, primary_key=True)
    conditions = Column(db.String, default="")

    def has_validated(self, value):
        list_conditions = self.conditions.split(",")
        return value in list_conditions

    def validates(self, value):
        if self.has_validated(value):
            pass
        else:
            if self.conditions:
                self.conditions += ",%s" % value
            else:
                self.conditions += str(value)

    def __str__(self):
        the_str = "User \"%s\":\n" % self.pseudo
        the_str += "\t- validated_conditions: %s" % self.conditions
        return the_str


class AuthProvider(metaclass=abc.ABCMeta):

    checkers = dict()

    def __init__(self, name, local_url_homepage, userModel):
        # Define logger
        self._logger = logging.getLogger(self.__class__.__name__)

        self.local_url_homepage = local_url_homepage
        self.name = name
        self.userModel = userModel

        try:
            current_app.add_url_rule(
                "/deco/<name>", "deco", self.__class__.disconnect_action
            )
        except AssertionError as e:
            pass

        self._logger.info("%s is loaded" % name)

        ProviderFactory().set(name, self)

    def connect(self, user):
        if self.userModel.__abstract__:
            self.session["user"] = user
        else:
            self.session["user"] = user.pseudo

    def disconnect(self):
        del self.session["user"]

    @classmethod
    def connect_checker(cls, checker_name, checker):
        AuthProvider.checkers[checker_name] = checker

    @classmethod
    def disconnect_action(cls, name):
        provider = ProviderFactory().get(name)

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
            return self.userModel.query.filter(
                self.userModel.pseudo == self.session["user"]
            ).first()

    def validates_connection(self, condition=None):
        if condition is not None:
            if (condition != "connected"):
                return (AuthProvider.checkers[condition](self.user), condition)
            else:
                return ("user" in self.session, "connected")
        else:
            validated = ("user" in self.session, "connected")
            if not validated[0]:
                return validated

            for checker_name in AuthProvider.checkers:
                if not AuthProvider.checkers[checker_name](self.user):
                    validated = (False, checker_name)
                    break

            return validated


    @property
    def url_deco(self):
        return make_global_url("/deco/" + self.name)

    @property
    def session(self):
        if "authprovider:" + str(self.name) not in flask_session.keys():
            flask_session["authprovider:" + str(self.name)] = {}

        return flask_session["authprovider:" + str(self.name)]
