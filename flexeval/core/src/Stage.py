# coding: utf8
# license : CeCILL-C

from flask import g, abort
from flask import url_for as flask_url_for
from flask import session as flask_session

from flexeval.utils import make_global_url

from .Module import Module
from .Config import Config
from .Provider import Provider

from .TemplateProvider import NotFoundError

class StageError(Exception):
    pass

class StageNotFound(StageError):
    pass

class ResolvedStageTemplate(StageError):

    def __init__(self,template_path):
        self.path = template_path

class Stage():

    def __init__(self,name,data=None):

        self.name = name

        try:
            self.params = Config().data()["stages"][name]
        except Exception as e:
            raise StageNotFound()

        self.mod_name = self.params["type"]
        self.mod_rep = self.params["type"].split(":")[0]

    def update(self,name,val):
        assert not(name == "type") and not(name == "name")

        if name not in Config().data()["stages"][self.name]:
            Config().data()["stages"][self.name][name] = None

        Config().data()["stages"][self.name][name] = val

    @property
    def session(self):
        if "stage:"+self.name not in flask_session.keys():
            flask_session["stage:"+self.name] = {}

        return flask_session["stage:"+self.name]

    @property
    def local_url_next(self):

        if "next" not in self.params:
            next_module = "/"
        else:

            if isinstance(self.params["next"],dict):
                next_module={}
                for next_module_name in self.params["next"].keys():
                    next_module[next_module_name] = Stage(self.params["next"][next_module_name]).local_url
            else:
                next_module = Stage(self.params["next"]).local_url

        return next_module

    def has_next_module(self):
        return "next" in self.params

    @property
    def template(self):
        if "template" in self.params:

            template = self.params["template"]

            try :
                template_path = Provider().get("templates").get(template)
            except NotFoundError as e:
                template_path = Provider().get("templates").get(template,"mod:"+str(self.mod_rep))

            return ResolvedStageTemplate(template_path)

        else:
            return None

    @property
    def variables(self):
        variables = {}

        if "variables" in self.params:
            variables = self.params["variables"]

        if "session_variable" in self.session:
            for session_variable_name in self.session["session_variable"].keys():
                variables[session_variable_name] = self.session["session_variable"][session_variable_name]

        return variables

    def get_variable(self,name,default_value):
        if not(name in self.variables):
            return default_value

        return self.variables[name]

    def set_variable(self,name,value):
        if not("session_variable" in self.session):
            self.session["session_variable"] = {}
        self.session["session_variable"][name] = value

    @property
    def local_url(self):
        return "/"+StageModule.name_type+"/"+self.mod_name+"/"+self.name+"/"

    def get(self,name):
        if name in self.params:
            return self.params[name]
        else:
            return None

class StageModule(Module):

    name_type = "stage"
    homepage = "/"

    def local_rule(self):
        return "/"+self.__class__.name_type+'/'+self.get_mod_name()+'/<stage_name>'

    @property
    def current_stage(self):
        return g.stage

    def render_template(self,template,next=None,**parameters):

        stage = self.current_stage

        args = {}
        args["THIS_MODULE"] = "mod:"+str(self.mod_rep)

        if isinstance(self.current_stage.local_url_next,dict):
            global_url_next = {}
            for local_url_next_name in self.current_stage.local_url_next:
                global_url_next[local_url_next_name] = make_global_url(self.current_stage.local_url_next[local_url_next_name])
            args["url_next"] = global_url_next
        else:
            args["url_next"] = make_global_url(self.current_stage.local_url_next)

        if isinstance(template,ResolvedStageTemplate):
            template = template.path
        else:
            template = Provider().get("templates").get(template,"mod:"+str(self.mod_rep))

        return super().render_template(template,args=args,parameters=parameters,variables=stage.variables)

    def url_for(self,endpoint,stage_name = None,**kwargs):
        if stage_name is None:
            stage_name = self.current_stage.name
        return flask_url_for(endpoint,stage_name = stage_name,**kwargs)

    def get_endpoint_for_local_rule(self,rule):
        return self.name+"."+"local_url@"+str(rule.replace(".","_"))

    def route(self,rule, **options):
        def decorated(func):
            def wrapper(*args, **kwargs):
                stage_name = kwargs["stage_name"]
                del kwargs["stage_name"]

                try:
                    g.stage = Stage(stage_name)
                except Exception as e:
                    abort(404)

                return func(*args, **kwargs)
            self.add_url_rule(rule,"local_url@"+str(rule.replace(".","_")),wrapper,**options)

            return wrapper

        return decorated
