# coding: utf8
# license : CeCILL-C

from flask import current_app

from .Provider import Provider

class AssetsProviderError(Exception):
    pass

class UnknowSourceError(AssetsProviderError):

    def __init__(self,path,_from):
        self.path = path
        self._from = _from

class AssetsProvider():

    __abstract__ = True

    def __init__(self,url_prefix):
        self.url_prefix = url_prefix
        current_app.add_url_rule(self.url_prefix+'/<path:path>',self.__class__.__name__+':assets:'+url_prefix,self.get_content)
        Provider().set("assets",self)
        print(" * AssetsProvider:"+self.__class__.__name__+" loaded and bound to: "+self.url_prefix)

    def url_flexeval(self,path):
        raise NotImplementedError()

    def url_mod(self,name_mod,path):
        raise NotImplementedError()

    def url_instance(self,path):
        raise NotImplementedError()

    def get_content(self,path):
        raise NotImplementedError()

    def local_url(self,path,_from=None):

        if not(path[0] == "/"):
            path = "/"+path

        if _from is None:
            return self.url_instance(path)
        elif _from == "flexeval":
            return self.url_flexeval(path)
        elif _from[:3] == "mod":
            return self.url_mod(_from[4:],path)
        else:
            raise UnknowSourceError(path,_from)
