# coding: utf8
# license : CeCILL-C

from pathlib import Path

from flask import current_app, g

from flexeval.utils import safe_copy_rep
from flexeval.core import TemplateProvider

class DefaultProvider(TemplateProvider):

    def register_flexeval(self):
        safe_copy_rep(current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/templates", self.folder+"/instance/")

    def register_instance(self):
        safe_copy_rep(current_app.config["FLEXEVAL_DIR"]+"/templates", self.folder+"/flexeval/")

    def register_module(self,name):
        safe_copy_rep(current_app.config["FLEXEVAL_DIR"]+"/mods/"+name+"/templates",self.folder+"/flexeval/mods/"+name)

    def template_loaded(self,rep,path):
        if not(hasattr(g,"loaded_template")):
            g.loaded_template = []

        if rep+":"+path in g.loaded_template:
            return True
        else:
            g.loaded_template.append(rep+":"+path)
            return False

    def get_flexeval(self,path):
        if Path(self.folder+"/instance/flexeval"+path).is_file() and not(self.template_loaded("flexeval",path)):
            return "/instance/flexeval"+path
        else:
            return "/flexeval"+path

    def get_mod(self,name_mod,path):
        if Path(self.folder+"/instance/flexeval/mods/"+str(name_mod)+path).is_file() and not(self.template_loaded("mods:"+str(name_mod),path)):
            return "/instance/flexeval/mods/"+str(name_mod)+path
        else:
            return "/flexeval/mods/"+str(name_mod)+path

    def get_instance(self,path):
        return "/instance"+path
