# coding: utf8
# license : CeCILL-C

import logging
from flexeval.utils import AppSingleton


class ProviderError(Exception):
    pass


class UndefinedError(ProviderError):
    def __init__(self, name_provider):
        self.name_provider = name_provider


class ProviderFactory(metaclass=AppSingleton):
    def __init__(self):
        # Define logger
        self._logger = logging.getLogger(self.__class__.__name__)
        self.providers = {}

    def get(self, name):
        try:
            return self.providers[name]
        except Exception as e:
            raise UndefinedError(name)

    def exists(self, name):
        return name in self.providers.keys()

    def set(self, name, provider):

        if ProviderFactory().exists(name):
            oldprovider = ProviderFactory().get(name)

            self._logger.warning(
                '%s is overwritten by %s for provider named "%s".'
                % (oldprovider.__class__.__name__, provider.__class__.__name__, name)
            )

        self.providers[name] = provider
