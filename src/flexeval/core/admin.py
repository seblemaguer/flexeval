from typing import Any, Callable, ParamSpec
from typing_extensions import override

from flask import abort
from flask import url_for as flask_url_for
from .module import Module

P = ParamSpec("P")


class AdminModule(Module):
    name_type = "admin"
    homepage = "/admin"

    @override
    def local_rule(self) -> str:
        return f"/{self.__class__.name_type}/{self.get_mod_name()}/"

    @override
    def render_template(
        self, path_template: str | None = None, args=dict(), variables=dict(), parameters=dict()
    ) -> str:
        args["THIS_MODULE"] = "mod:" + str(self.mod_rep)

        # Add experience variables
        filled_variables: dict[str, Any] = self._config["variables"]
        for key, variable in variables.items():
            filled_variables[key] = variable

        return super().render_template(
            path_template=path_template, args=args, parameters=parameters, variables=filled_variables
        )

    @override
    def url_for(self, endpoint: str, **kwargs: Any) -> str:
        return flask_url_for(endpoint, **kwargs)

    def get_endpoint_for_local_rule(self, rule: str):
        return f"{self.name}.local_url@{rule.replace('.', '_')}"

    @override
    def route(self, rule: str, **options: Any) -> Callable[..., Any]:
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

    def local_url(self) -> str:
        return f"{self.__class__.name_type}/{self.get_mod_name()}/"
