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

from flexeval.core import TemplateProvider


class DefaultProvider(TemplateProvider):
    """Default template provide factory
    """

    def register_flexeval(self):
        copytree(
            current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/templates",
            self.folder + "/instance/",
            dirs_exist_ok=True,
        )

    def register_instance(self):
        copytree(
            current_app.config["FLEXEVAL_DIR"] + "/templates",
            self.folder + "/flexeval/",
            dirs_exist_ok=True,
        )

    def register_module(self, name):
        copytree(
            current_app.config["FLEXEVAL_DIR"] + "/mods/" + name + "/templates",
            self.folder + "/flexeval/mods/" + name,
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

    def get_flexeval(self, path):
        if Path(self.folder + "/instance/flexeval" + path).is_file() and \
           (not self.template_loaded("flexeval", path)):
            return "/instance/flexeval" + path
        else:
            return "/flexeval" + path

    def get_mod(self, name_mod, path):
        if Path(
            self.folder + "/instance/flexeval/mods/" + str(name_mod) + path
        ).is_file() and not (self.template_loaded("mods:" + str(name_mod), path)):
            return "/instance/flexeval/mods/" + str(name_mod) + path
        else:
            return "/flexeval/mods/" + str(name_mod) + path

    def get_instance(self, path):
        return "/instance" + path
