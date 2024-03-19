# coding: utf8
# license : CeCILL-C

from flask import abort
from flask import url_for as flask_url_for

from .Module import Module
from .Config import Config

from .providers import provider_factory


class AdminModule(Module):
    name_type = "admin"
    homepage = "/admin"

    @classmethod
    def get_all_admin_modules(cls):
        return Config().admin_modules

    @classmethod
    def get_local_url_for(cls, name):
        return "/" + cls.name_type + "/" + name + "/"

    @classmethod
    def get_config_for(cls, name):
        for mod in Config().data()["admin"]["mods"]:
            if mod["mod"] == name:
                return mod
        return None

    def get_config(self):
        return self.__class__.get_config_for(self.get_mod_name())

    def local_rule(self):
        return "/" + self.__class__.name_type + "/" + self.get_mod_name() + "/"

    def render_template(self, template, next=None, **parameters):
        args = {}
        args["THIS_MODULE"] = "mod:" + str(self.mod_rep)

        variables = {}
        try:
            variables = self.get_config()["variables"]
        except Exception:
            pass

        template = provider_factory.get("templates").get(template)  # "mod:" + str(self.mod_rep)
        return super().render_template(template, args=args, parameters=parameters, variables=variables)

    def url_for(self, endpoint, **kwargs):
        return flask_url_for(endpoint, **kwargs)

    def get_endpoint_for_local_rule(self, rule):
        return self.name + "." + "local_url@" + str(rule.replace(".", "_"))

    def route(self, rule, **options):
        def decorated(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.add_url_rule(rule, "local_url@" + str(rule.replace(".", "_")), wrapper, **options)

            return wrapper

        return decorated

    def valid_connection_required(self, f):
        def wrapper(*args, **kwargs):
            (user_validates, condition) = self.authProvider.validates_connection()

            if not user_validates:
                if (condition is None) or (condition == "connected"):
                    abort(401)
                # else:
                #     raise Exception("No handler to deal with invalid condition \"%s\"" % condition)

            return f(*args, **kwargs)

        return wrapper
