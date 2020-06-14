# coding: utf8
# license : CeCILL-C

from pathlib import Path

from flask import current_app

from .Provider import Provider


class TemplateProviderError(Exception):
    pass

class ImportError(TemplateProviderError):

    def __init__(self,message):
        self.message = message

class UnknowSourceError(TemplateProviderError):
    pass

class NotFoundError(TemplateProviderError):

    def __init__(self,file):
        self.file = file

class TemplateProvider():

    __abstract__ = True

    def __init__(self, folder):

        self.folder = folder
        current_app.template_folder = self.folder

        try:
            self.register_flexeval()
        except Exception as e:
            raise ImportError("Import from flexeval's templates failed.")

        try:
            self.register_instance()
        except Exception as e:
            raise ImportError("Import from instance's templates failed.")

        Provider().set("templates",self)
        print(" * TemplateProvider:"+self.__class__.__name__+" loaded. ")


    def register(self,name_module):
        try:
            self.register_module(name_module)
        except Exception as e:
            raise ImportError("Import from mod:"+name_module+" failed.")

    def register_flexeval(self):
        raise NotImplementedError()

    def register_instance(self):
        raise NotImplementedError()

    def register_module(self,name):
        raise NotImplementedError()

    def get_flexeval(self,path):
        raise NotImplementedError()

    def get_mod(self,name_mod,path):
        raise NotImplementedError()

    def get_instance(self,path):
        raise NotImplementedError()

    def get(self,path,_from=None):

        if not(path[0] == "/"):
            path = "/"+path

        if _from is None:
            template_url_file = self.get_instance(path)
        elif _from == "flexeval":
            template_url_file =  self.get_flexeval(path)
        elif _from[:3] == "mod":
            template_url_file = self.get_mod(_from[4:],path)
        else:
            raise UnknowSourceError()

        if not(Path(self.folder+template_url_file).is_file()):
            raise NotFoundError(self.folder+template_url_file)

        return template_url_file
