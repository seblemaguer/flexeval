# coding: utf8
# license : CeCILL-C

import os
import errno

import abc

from pathlib import Path

from flask import current_app

from flexeval.core import ProviderFactory


class TemplateProviderError(Exception):
    pass


class ImportError(TemplateProviderError):
    def __init__(self, message):
        self.message = message


class UnknowSourceError(TemplateProviderError):
    pass


class TemplateProvider(metaclass=abc.ABCMeta):
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

        ProviderFactory().set("templates", self)
        print(" * TemplateProvider:" + self.__class__.__name__ + " loaded. ")

    def register(self, name_module):
        try:
            self.register_module(name_module)
        except Exception as e:
            raise ImportError("Import from mod:" + name_module + " failed.")

    def get(self, path):

        if not (path[0] == "/"):
            path = "/" + path

        if not (Path(self.folder + path).is_file()):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                os.path.join(self.folder, path),
            )

        return path
