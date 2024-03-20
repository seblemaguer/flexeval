from typing import Any, Callable, ParamSpec
from typing_extensions import override

from flask import abort
from flask import url_for as flask_url_for
from .module import Module
from .Config import Config

from .providers import provider_factory, TemplateProvider

P = ParamSpec("P")


class AdminModule(Module):
    name_type = "admin"
    homepage = "/admin"

    def get_config(self) -> dict[str, Any]:
        return self.__class__.get_config_for(self.get_mod_name())

    @override
    def local_rule(self) -> str:
        return f"/{self.__class__.name_type}/{self.get_mod_name()}/"

    @override
    def render_template(self, path_template: str, args=dict(), parameters=dict(), variables=dict()) -> str:
        args = {}
        args["THIS_MODULE"] = "mod:" + str(self.mod_rep)

        variables = {}
        try:
            variables = self.get_config()["variables"]
        except Exception:
            pass

        provider: TemplateProvider = provider_factory.get(TemplateProvider.NAME)  # type: ignore
        path_template: str = provider.get(path_template)  # "mod:" + str(self.mod_rep)
        return super().render_template(path_template, args=args, parameters=parameters, variables=variables)

    @override
    def url_for(self, endpoint: str, **kwargs) -> str:  # type: ignore
        return flask_url_for(endpoint, **kwargs)

    def get_endpoint_for_local_rule(self, rule: str):
        return f"{self.name}.local_url@{rule.replace('.', '_')}"

    @override
    def route(self, rule: str, **options: Any) -> Callable[Any, Any]:
        def decorated(f: Callable[P, Any]) -> Any:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                return f(*args, **kwargs)

            self.add_url_rule(rule, "local_url@" + str(rule.replace(".", "_")), wrapper, **options)

            return wrapper

        return decorated

    @override
    def valid_connection_required(self, f: Callable[P, bool]) -> Callable[P, bool]:
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            (user_validates, condition) = self.auth_provider.validates_connection()

            if not user_validates:
                if condition == "connected":
                    abort(401)
                # else:
                #     raise Exception("No handler to deal with invalid condition \"%s\"" % condition)

            return f(*args, **kwargs)

        return wrapper

    @classmethod
    def get_all_admin_modules(cls):
        return Config().admin_modules

    @classmethod
    def get_local_url_for(cls, name: str) -> str:
        return f"/{cls.name_type}/{name}/"

    @classmethod
    def get_config_for(cls, name):
        for mod in Config().data()["admin"]["mods"]:
            if mod["mod"] == name:
                return mod
        return None
