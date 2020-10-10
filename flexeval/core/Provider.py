# coding: utf8
# license : CeCILL-C

from flexeval.utils import AppSingleton

class ProviderError(Exception):
    pass

class UndefinedError(ProviderError):

    def __init__(self,name_provider):
        self.name_provider = name_provider

class Provider(metaclass=AppSingleton):

    def __init__(self):
        self.providers={}

    def get(self,name):
        try:
            return self.providers[name]
        except Exception as e:
            raise UndefinedError(name)

    def exists(self,name):
        return name in self.providers.keys()

    def set(self,name,provider):

        if Provider().exists(name):
            oldprovider =  Provider().get(name)

            print(" * [OVERWRITE] "+oldprovider.__class__.__name__+" >> "+provider.__class__.__name__+" for provider named:"+name+" .")

        self.providers[name] = provider
