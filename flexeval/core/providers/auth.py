"""Module providing elementary helpers to authenticate in FlexEval
"""

# Python
from typing_extensions import override
from typing import Callable, Any
import random
import abc

# Flask
from flask import session as flask_session
from flask import current_app, redirect
from werkzeug.wrappers import Response

# Flexeval
from flexeval.database import Column, db
from flexeval.utils import make_global_url
from .base import provider_factory, Provider  # FIXME: provider_factory is not great here, it should be removed


class AuthProviderError(Exception):
    """The generic error of any authentication provider"""

    pass


class NotConnectedError(Exception):
    """The error indicating an issue during the connection phase of the provider"""

    pass


class UserModel:
    """The model of User

    A user is at least a participant, but this can be extended if needed.
    This class needs to be extended to cover the needs of your authentication methodology.
    """

    id = Column(db.String, primary_key=True)
    conditions = Column(db.String, default="")

    def has_validated(self, condition: str) -> bool:
        """Check if the user already validated the given condition

        Parameters
        ----------
        value : str
            the condition to check

        Returns
        -------
        bool
            True if the condition is validated, False if not
        """

        list_conditions = self.conditions.split(",")
        return condition in list_conditions

    def validates(self, condition: str):
        """Record that the user validates the given condition

        Parameters
        ----------
        condition : str
            the given condition the user validates

        """

        if self.has_validated(condition):
            pass
        else:
            if self.conditions:
                self.conditions += ",%s" % condition
            else:
                self.conditions += str(condition)

    @override
    def __str__(self):
        the_str = f'User "{self.id}":\n'
        the_str += f"\t- validated_conditions: {self.conditions}"
        return the_str


class AuthProvider(Provider, metaclass=abc.ABCMeta):
    """Default authentication provider"""

    checkers: dict[str, Callable[[UserModel], bool]] = dict()

    def __init__(self, name: str, local_url_homepage: str | None, user_model: UserModel | None):
        """Initialisation method

        Parameters
        ----------
        name : str
            The name of the authentication module
        local_url_homepage : str
            The local URL of the module requiring the authentication
        user_model : UserModel
            The user model
        """

        super().__init__()
        self.local_url_homepage = local_url_homepage
        self.name = name
        self.user_model = user_model
        self._logger.debug(f"Initialisation with (name = {name}, local_url_homepage = {local_url_homepage})")

        try:
            current_app.add_url_rule("/deco/<name>", "deco", self.__class__.disconnect_action)
        except AssertionError:
            pass

        self._logger.info("%s is loaded" % name)

        provider_factory.set(name, self)

    def connect(self, user: UserModel):
        """Connect a user

        This is done by simply adding the user to the session dictionnary

        Parameters
        ----------
        user : UserModel
            The user to connect
        """

        if self.user_model.__abstract__:  # type: ignore
            self.session["user"] = user
        else:
            self.session["user"] = user.id

    def disconnect(self):
        """Disconnect the user

        This is done by simply removing the user to the session dictionnary
        """
        del self.session["user"]

    def validates_connection(self, condition: str | None = None) -> tuple[bool, str]:
        """Check if the user already validated the given condition

        Parameters
        ----------
        condition : str or None
            The optional condition to check to validate the connection

        Returns
        -------
        Tuple[bool, str]
            - True if the connection is validated, False if not
            - the checker name
        """

        if condition is not None:
            if condition != "connected":
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

    @classmethod
    def connect_checker(cls, checker_name: str, checker: Callable[[UserModel], bool]):
        """Add a checking routine providing a dynamic condition to validate during the connection

        Parameters
        ----------
        checker_name : str
            the name of the checker
        checker : Callable
            the checking function which will be called during the
            connection
        """
        AuthProvider.checkers[checker_name] = checker

    @classmethod
    def disconnect_action(cls, name: str) -> Response:
        """Disconnect (log-out) the user

        Parameters
        ----------
        name : str
            the name of the provider

        Returns
        -------
        Response
            The flask Response object redirecting the client to the
            proper page after the disconnect
        """
        provider: Provider = provider_factory.get(name)
        if not isinstance(provider, AuthProvider):
            raise Exception(f"{name} is not an authentication provider (type = {provider.__class__})")

        provider.disconnect()
        return redirect(provider.local_url_homepage)  # type: ignore

    @property
    def user(self) -> UserModel:
        """Provide an easy way to access the user information

        Returns
        -------
        UserModel
            The model of the user
        """
        if self.user_model.__abstract__:  # type: ignore
            return self.session["user"]
        else:
            return self.user_model.query.filter(self.user_model.id == self.session["user"]).first()  # type: ignore

    @property
    def url_deco(self) -> str:
        """Generates the disconnect address

        Returns
        -------
        str
            The global URL to disconnect the current user
        """
        return make_global_url("/deco/" + self.name)

    @property
    def session(self) -> dict[str, Any]:
        """Provides a convenient wrapper to the flask session for the provider

        Returns
        -------
        Dict[str, Any]
            the session dictionary
        """
        if "authprovider:" + str(self.name) not in flask_session.keys():
            flask_session["authprovider:" + str(self.name)] = {}

        return flask_session["authprovider:" + str(self.name)]


class AnonAuthProvider(AuthProvider):
    """A default anonymous user authentification provider"""

    __userBase__ = UserModel

    @override
    def connect(self):  # type: ignore
        """Connect a user

        The user ID will respect the pattern <anon@XXX> where XXX is a random number
        """
        user_id = "anon@" + str(random.randint(1, 999999999999999))
        super().connect(self.user_model.create(id=user_id))  # type: ignore

    @override
    def validates_connection(self, condition: str | None = None) -> tuple[bool, str]:
        """Check if the user already validated the given condition

        Parameters
        ----------
        condition : str or None
            The optional condition to check to validate the connection

        Returns
        -------
        Tuple[bool, str]
            - True if the connection is validated, False if not
            - the checker name
        """

        if not (super().validates_connection("connected")[0]):
            self.connect()

        return super().validates_connection(condition)

    @override
    def disconnect(self):
        pass


class VirtualAuthProvider(AuthProvider):
    """A virtual user authentication provider.

    A virtual authentication provider is only used a place holder before the definition of the
    actual authentication provider.
    """

    __userBase__ = None

    def __init__(
        self,
        name: str | None = None,
        local_url_homepage: str | None = None,
        userModel: UserModel | None = None,
    ):
        """Initialisation method

        Parameters
        ----------
        name : str
            The name of the authentication module
        local_url_homepage : str
            The local URL of the module requiring the authentication
        user_model : UserModel
            The user model
        """
        if name is None:
            pass
        else:
            super(VirtualAuthProvider, self).__init__(name, local_url_homepage, userModel)

    @override
    def connect(self, user: UserModel):
        """A virtual user can't connect,

        Raises
        ------
        NotConnectedError
           all the time, as you can't connect a virtual user
        """
        raise NotConnectedError()

    @override
    def validates_connection(self, condition: str | None = None) -> tuple[bool, str]:
        """Always returns (False, "connected")

        Parameters
        ----------
        condition : Optional[str]
            this is ignored

        Returns
        -------
        Tuple[bool, str]
            always (False, "connected")
        """
        return (False, "connected")
