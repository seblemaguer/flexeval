# Import Libraries
from flask import current_app,request

from perceval.core import StageModule
from perceval.database import ModelFactory,Column,ForeignKey,db,relationship
from perceval.utils import redirect

from .model import Form

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
