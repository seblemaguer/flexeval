# coding: utf8
from pathlib import Path

from flask import current_app, g

from perceval.utils import safe_copy_rep
from perceval.core import TemplateProvider

class DefaultProvider(TemplateProvider):

    def register_perceval(self):
        safe_copy_rep(current_app.config["PERCEVAL_INSTANCE_DIR"]+"/templates", self.folder+"/instance/")

    def register_instance(self):
        safe_copy_rep(current_app.config["PERCEVAL_DIR"]+"/templates", self.folder+"/perceval/")

    def register_module(self,name):
        safe_copy_rep(current_app.config["PERCEVAL_DIR"]+"/mods/"+name+"/templates",self.folder+"/perceval/mods/"+name)

    def template_loaded(self,rep,path):
        if not(hasattr(g,"loaded_template")):
            g.loaded_template = []

        if rep+":"+path in g.loaded_template:
            return True
        else:
            g.loaded_template.append(rep+":"+path)
            return False

    def get_perceval(self,path):
        if Path(self.folder+"/instance/perceval"+path).is_file() and not(self.template_loaded("perceval",path)):
            return "/instance/perceval"+path
        else:
            return "/perceval"+path

    def get_mod(self,name_mod,path):
        if Path(self.folder+"/instance/perceval/mods/"+str(name_mod)+path).is_file() and not(self.template_loaded("mods:"+str(name_mod),path)):
            return "/instance/perceval/mods/"+str(name_mod)+path
        else:
            return "/perceval/mods/"+str(name_mod)+path

    def get_instance(self,path):
        return "/instance"+path
