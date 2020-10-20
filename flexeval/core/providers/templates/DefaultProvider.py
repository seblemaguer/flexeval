# coding: utf8
# license : CeCILL-C

import sys
py_version = sys.version_info
if (py_version.major >= 3) and (py_version.minor >= 8):
    from shutil import copytree
else:
    from flexeval.utils import copytree

from pathlib import Path

from flask import current_app, g

from .TemplateProvider import TemplateProvider


class DefaultProvider(TemplateProvider):
    """Default template provide factory
    """

    def register_flexeval(self):
        copytree(
            current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/templates",
            self.folder,
            dirs_exist_ok=True,
        )

    def register_instance(self):
        copytree(
            current_app.config["FLEXEVAL_DIR"] + "/templates",
            self.folder,
            dirs_exist_ok=True,
        )

    def register_module(self, name):
        copytree(
            current_app.config["FLEXEVAL_DIR"] + "/mods/" + name + "/templates",
            self.folder,
            dirs_exist_ok=True,
        )

    def template_loaded(self, rep, path):
        if not (hasattr(g, "loaded_template")):
            g.loaded_template = []

        if rep + ":" + path in g.loaded_template:
            return True
        else:
            g.loaded_template.append(rep + ":" + path)
            return False
