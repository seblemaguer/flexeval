# coding: utf8
# license : CeCILL-C

# Import Libraries
import json

import threading

from flask import current_app, request

from flexeval.core import campaign_instance
from flexeval.database import ModelFactory, db
from flexeval.utils import redirect

from .model import Form

sem_form = threading.Semaphore()


class FormError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message: str = message


class FileNotFound(FormError):
    pass


class MalformationError(FormError):
    pass


with campaign_instance.register_stage_module(__name__) as sm:

    @sm.route("/", methods=["GET"])
    @sm.valid_connection_required
    def main_default():
        # Get the current stage and the user
        stage = sm.current_stage

        # Create Form table and link the user to this form
        if ModelFactory().has(stage.name, Form):
            form_stage = ModelFactory().get(stage.name, Form)
            user = sm.auth_provider.user
            res = form_stage.query.filter_by(user_id=user.id)
            if res.first() is None:
                return sm.render_template(path_template=stage.template)
            else:
                next_urls: dict[str, str] = stage.next_local_urls
                if len(next_urls.keys()) > 1:
                    raise Exception("")
                stage_name = list(next_urls.keys())[0]
                return redirect(next_urls[stage_name])
        else:
            return sm.render_template(path_template=stage.template)

    @sm.route("/save", methods=["POST"])
    @sm.valid_connection_required
    def save():
        stage = sm.current_stage
        userModel = sm.auth_provider.user

        sem_form.acquire()
        if not ModelFactory().has(stage.name, Form):
            form_stage = ModelFactory().create(stage.name, Form)
        else:
            form_stage = ModelFactory().get(stage.name, Form)
        userModel.addRelationship(form_stage.__name__, form_stage, uselist=False)

        user = sm.auth_provider.user
        user_form_for_this_stage = getattr(user, form_stage.__name__)

        if user_form_for_this_stage is None:
            resp = form_stage.create(user_id=user.id)
            try:
                for field_key in request.form.keys():
                    form_stage.addColumn(field_key, db.String)
                    resp.update(**{field_key: request.form[field_key]})

                for field_key in request.files.keys():
                    form_stage.addColumn(field_key, db.BLOB)
                    with request.files[field_key].stream as f:
                        resp.update(**{field_key: f.read()})

            except Exception:
                resp.delete()

        sem_form.release()

        next_urls: dict[str, str] = stage.next_local_urls
        if len(next_urls.keys()) > 1:
            raise Exception("")
        stage_name = list(next_urls.keys())[0]
        return redirect(next_urls[stage_name])


with campaign_instance.register_stage_module(__name__, subname="autogen") as sm_autogen:

    @sm_autogen.route("/", methods=["GET"])
    @sm_autogen.valid_connection_required
    def main_autogen():
        stage = sm_autogen.current_stage

        # On récup le json
        try:
            with open(
                current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/" + stage.get("data"),
                encoding="utf-8",
            ) as form_json_data:
                form_json_data = json.load(form_json_data)
        except Exception:
            raise FileNotFound(
                "Issue when loading: " + current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/" + stage.get("data")
            )

        names = []
        for component in form_json_data["components"]:
            if "id" not in component:
                raise MalformationError(
                    "An ID is required for each component in "
                    + current_app.config["FLEXEVAL_INSTANCE_DIR"]
                    + "/"
                    + stage.get("data")
                )

            if not (component["id"].replace("_", "").isalnum()):
                raise MalformationError(
                    "ID: " + component["id"] + " is incorrect. Only alphanumeric's and '_' symbol caracteres are allow."
                )

            if component["id"] in names:
                raise MalformationError("ID: " + component["id"] + " is already defined.")

            names.append(component["id"])

        # On ajoute le template à l'étape
        stage.update("template", "dynamicForm.tpl")
        stage.set_variable("form_json_data", form_json_data)

        return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))
