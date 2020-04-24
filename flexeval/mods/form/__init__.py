# coding: utf8
# license : CeCILL-C

# Import Libraries
import json

from flask import current_app,request

from flexeval.core import StageModule
from flexeval.database import ModelFactory,Column,ForeignKey,db,relationship
from flexeval.utils import redirect

from .model import Form

class FormError(Exception):
    def __init__(self,message):
        self.message = message

class FileNotFound(FormError):
    pass

class MalformationError(FormError):
    pass

with StageModule(__name__) as sm:

    @sm.route("/", methods = ['GET'])
    @sm.connection_required
    def main():
        stage = sm.current_stage
        userModel = sm.authProvider.userModel

        # Form établie une relation FormStage -> User
        FormStage = ModelFactory().create(stage.name,Form)

        # On établie la relation User -> FormStage
        userModel.addRelationship(FormStage.__name__,FormStage,uselist=False)

        # Lorsque l'on utilise sm.authProvider.user on créée une nouvelle instance de UserModel
        # Cette instance est impacté par les changements précédants
        user = sm.authProvider.user
        user_form_for_this_stage = getattr(user,FormStage.__name__)

        if user_form_for_this_stage is None:
            return sm.render_template(template=stage.template)
        else:
            return redirect(stage.local_url_next)

    @sm.route("/save", methods = ['POST'])
    @sm.connection_required
    def save():
        stage = sm.current_stage
        FormStage = ModelFactory().get(stage.name,Form)

        if FormStage is None:
            return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

        user = sm.authProvider.user
        user_form_for_this_stage = getattr(user,FormStage.__name__)

        if user_form_for_this_stage is None:
            resp = FormStage.create(user_pseudo=user.pseudo)
            try:
                for field_key in request.form.keys():
                    FormStage.addColumn(field_key,db.String)
                    resp.update(**{field_key:request.form[field_key]})

                for field_key in request.files.keys():
                    FormStage.addColumn(field_key,db.BLOB)
                    with request.files[field_key].stream as f:
                        resp.update(**{field_key:f.read()})

            except Exception as e:
                resp.delete()

        return redirect(stage.local_url_next)

with StageModule(__name__,subname="autogen") as sm_autogen:

    @sm_autogen.route("/", methods = ['GET'])
    @sm_autogen.connection_required
    def main():

        stage = sm_autogen.current_stage

        # On récup le json
        try:
            with open(current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/'+stage.get("data"),encoding='utf-8') as form_json_data:
                form_json_data = json.load(form_json_data)
        except Exception as e:
            raise FileNotFound("Issue when loading: "+current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/'+stage.get("data") )

        names = []
        for component in form_json_data["components"]:
            if ("id" not in component):
                raise MalformationError("An ID is required for each component in "+current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/'+stage.get("data"))

            if not(component["id"].replace("_","").isalnum()):
                raise MalformationError("ID: "+component["id"]+" is incorrect. Only alphanumeric's and '_' symbol caracteres are allow.")

            if component["id"] in names:
                raise MalformationError("ID: "+component["id"]+" is already defined.")

            names.append(component["id"])

        # On ajoute le template à l'étape
        stage.update("template","dynamicForm.tpl")
        stage.set_variable("form_json_data",form_json_data)

        return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))
