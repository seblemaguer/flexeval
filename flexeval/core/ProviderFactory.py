"""
flexeval.core.ProviderFactory
=============================

Mpdule which provides baseline classes to manage providers
"""

import logging

from flexeval.utils import AppSingleton


class ProviderError(Exception):
    """Baseline exception class for any erroces caused by a provider."""

    pass


class UndefinedError(ProviderError):
    """Exception raised if the wanted provider is undefined

    Attributes
    ----------
    name_provider: string
        The name to which no provider is corresponding to.
    """

    def __init__(self, name_provider):
        self.name_provider = name_provider


class ProviderFactory(metaclass=AppSingleton):
    """Factory class to generate providers

    Attributes
    ----------
    _logger: Logger
        The internal logger
    providers: dict
        The dictionnary associating the provider name to its instance
    """

    def __init__(self):
        """Constructor"""

        # Define logger
        self._logger = logging.getLogger(self.__class__.__name__)
        self.providers = {}

    def get(self, name):
        """Method to get the provider given its name.

        Parameters
        ----------
        self: ProviderFactory
            The current object
        name: string
            The name of the wanted provider

        Returns
        -------
        ????: the provider

        Raises
        ------
        UndefinedError: if there is no providers corresponding to the given name
        """
        try:
            return self.providers[name]
        except Exception:
            raise UndefinedError(name)

    def exists(self, name):
        """Method to check if there is a provider corresponding to a given
        name.

        Parameters
        ----------
        self: ProviderFactory
            The current object
        name: string
            The name of the provider

        Returns
        -------
        bool: true if a provider exists, false else
        """
        return name in self.providers.keys()

    def set(self, name, provider):
        """Method to associate a given provider to a given name.

        If the given name already has a provider associated to it, this provider will be replaced.

        Parameters
        ----------
        self: ProviderFactory
            The current object
        name: string
            The name of the provider
        provider: ???
            The provider
        """
        if ProviderFactory().exists(name):
            oldprovider = ProviderFactory().get(name)
            old_name = oldprovider.__class__.__name__
            self._logger.debug(
                f'{old_name} is overwritten by {provider.__class__.__name__} for provider named "{name}".'
            )

        self.providers[name] = provider
