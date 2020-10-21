# coding: utf8
# license : CeCILL-C

import sys
import os
import errno

py_version = sys.version_info
if (py_version.major >= 3) and (py_version.minor >= 8):
    from shutil import copytree
else:
    from flexeval.utils import copytree

import glob

from pathlib import Path

from flask import current_app, g

from flexeval.core import ProviderFactory


class TemplateProviderError(Exception):
    pass


class ImportError(TemplateProviderError):
    def __init__(self, message):
        self.message = message


class UnknowSourceError(TemplateProviderError):
    pass


class TemplateProvider:
    def __init__(self, folder):

        self._instance_files = []
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

    def register_flexeval(self):
        copytree(
            current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/templates",
            self.folder,
            dirs_exist_ok=True,
        )

    def register_instance(self):

        # Save instance templates path to not replace them when registering mods
        tpl_dir = current_app.config["FLEXEVAL_DIR"] + "/templates"
        self._instance_files = [f.replace(tpl_dir + "/", "") for f in glob.glob(tpl_dir + '/**/*', recursive=True)]

        copytree(
            tpl_dir,
            self.folder,
            dirs_exist_ok=True,
        )

    def register_module(self, name):
        def ignore_instance(src, names):
            return set(names).intersection(set(self._instance_files))

        copytree(
            current_app.config["FLEXEVAL_DIR"] + "/mods/" + name + "/templates",
            self.folder,
            dirs_exist_ok=True,
            ignore=ignore_instance
        )

    def template_loaded(self, rep, path):
        if not (hasattr(g, "loaded_template")):
            g.loaded_template = []

        if rep + ":" + path in g.loaded_template:
            return True
        else:
            g.loaded_template.append(rep + ":" + path)
            return False
