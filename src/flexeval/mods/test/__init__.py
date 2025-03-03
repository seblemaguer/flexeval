# coding: utf8

from werkzeug import Response
from flask import request, abort

# Flexeval
from flexeval.core import campaign_instance
from flexeval.utils import redirect
from flexeval.database import commit_all

# Current package
from .src import test_manager, TransactionalObject


class TestsAlternateError(Exception):
    pass


class MalformationError(TestsAlternateError):
    def __init__(self, message):
        self.message = message


with campaign_instance.register_stage_module(__name__) as sm:

    @sm.route("/", methods=["GET"])
    @sm.valid_connection_required
    def main():
        """Entry point for the Test

        This function prepare the template and defines some key helper
        internal functions to generate the information required during
        the save stage. These functions are:
          - get_syssamples which provides the list of selected samples per *given system*
          - save_field_name which *has to be called* to get the field value (score, preference selection...)
            during the saving

        """

        # Get the current Stage and the corresponding test
        stage = sm.current_stage
        if not test_manager.has(stage.name):
            test = test_manager.register(stage.name, stage)
        else:
            test = test_manager.get(stage.name)

        # Define steps information
        nb_systems_per_step = int(stage["nb_systems_per_step"]) if ("nb_systems_per_step" in stage) else 1
        if nb_systems_per_step <= 0:
            nb_systems_per_step = len(list(test.systems.keys()))

        max_steps = int(stage["nb_steps"])  # TODO: add a default if ("nb_steps" in stage) else 0
        nb_steps_intro: int = int(stage["nb_steps_intro"]) if ("nb_steps_intro" in stage) else 0

        # Load transaction information
        transaction_timeout_seconds = stage["transaction_timeout_seconds"]
        if transaction_timeout_seconds is not None:
            test.set_timeout_for_transaction(int(transaction_timeout_seconds))

        # Get the user
        user = sm.auth_provider.user

        # Get the current step
        cur_step = test.nb_steps_complete_by(user)

        # Find out the current step is an introduction or not
        intro_step = False
        if cur_step < nb_steps_intro:
            intro_step = True
        else:
            intro_step = False

        if cur_step < max_steps:
            syssamples_for_this_step = test.get_step(
                cur_step, user, nb_systems=nb_systems_per_step, is_intro_step=intro_step
            )

            def _get_syssamples(*system_names):
                systems = []
                if len(system_names) == 0:
                    for syssample in syssamples_for_this_step.values():
                        systems.append(syssample)
                else:
                    for name_system in system_names:
                        systems.append(syssamples_for_this_step[name_system])

                return systems

            def _save_field_name(name: str, syssamples, record_name: str | None = None):
                name = name.replace(TransactionalObject.RECORD_SEP, "_")

                # Make sure the record exist and get a real name if record name is None
                user = sm.auth_provider.user
                record_name = test.get_record(user, record_name)

                # ID of the field
                ID = TransactionalObject.RECORD_SEP.join(
                    ["save", record_name, name] + [syssample.ID for syssample in syssamples]
                )

                # Associate field to record
                _ = test.add_field_to_record(user, ID, record_name)

                return ID

            def _prepare_new_record(name: str):
                # Record new record for current step and current user
                user = sm.auth_provider.user
                _ = test.create_new_record(user, name)
                return name

            # sm.logger.debug(f"Sample selected for this step are {get_syssamples()}")

            # Update information related to the steps
            if intro_step:
                max_steps = nb_steps_intro
                cur_step += 1
            else:
                max_steps = max_steps - nb_steps_intro
                cur_step = cur_step + 1 - nb_steps_intro

            parameters = {
                "max_steps": max_steps,
                "step": cur_step,
                "intro_step": intro_step,
                "syssamples": _get_syssamples,
                "field_name": _save_field_name,
                "new_record": _prepare_new_record,
            }

            # Complete the parameters with additional config
            for k in stage.keys():
                if (k not in parameters) and (k.lower() != "template"):
                    parameters[k] = stage.get(k)

            return sm.render_template(path_template=stage.template, parameters=parameters)
        else:
            next_urls: dict[str, str] = stage.next_local_urls
            if len(next_urls.keys()) > 1:
                raise Exception("More than one folloing URL is not yet supported for a step of a test")
            stage_name = list(next_urls.keys())[0]
            return redirect(next_urls[stage_name])

    @sm.route("/save", methods=["POST"])
    @sm.valid_connection_required
    def save() -> Response:
        """Saving routine of the test

        This method is called after the submission of the form
        implemented in the template associated to the step of the
        test.
        This method does:
          0. requiring a exclusive access to the db to avoid concurrency issue
          1. parsing the values of each *field* recorded by the method =save_field_name*
          2. filling the database *and creating new columns if necessary!*

        """
        stage = sm.current_stage
        test = test_manager.get(stage.name)  # TestManager(stage).get(stage.name)
        user = sm.auth_provider.user
        skip_after_n_step = stage.get("skip_after_n_step")

        # Log the request form for debugging purposes
        sm.logger.debug("#### The request form ####")
        sm.logger.debug(request.form)  # TODO: prettify!
        sm.logger.debug("#### <END>The request form ####")

        # Initialize the number of intro steps
        nb_steps_intro: int = int(stage["nb_steps_intro"]) if ("nb_steps_intro" in stage) else 0
        cur_step: int = test.nb_steps_complete_by(user)

        # Validate is the current step is an introduction step
        intro_step = False
        if nb_steps_intro > cur_step:
            intro_step = True

        # Fail if there is no transactions associated to the user
        if not test.has_transaction(user):
            abort(408)

        # Save
        all_records = test.get_all_records(user)
        for _, all_field_names in all_records.items():

            try:
                # Save responses from the user
                for field_type, field_list in [
                    ("string", request.form),
                    ("file", request.files),
                ]:
                    for field_key in field_list.keys():
                        if field_key in all_field_names:
                            # Several values can be returned for one key (MultiDict)
                            #    -> use d.get_list(key) instead d[key]
                            if len(field_list.getlist(field_key)) > 1:
                                field_value = str(field_list.getlist(field_key))
                            else:
                                field_value = field_list[field_key]

                            # Get the name of the info to save
                            if field_key[:5] == "save:":
                                field_key = field_key[5:]
                                (
                                    _,
                                    field_name,
                                    obfuscated_sample,
                                ) = field_key.split(TransactionalObject.RECORD_SEP)
                                name_col = field_name
                            else:
                                name_col = field_key
                                raise Exception("For now this is not supported")

                            # Extract the sample information
                            system, syssample_id = test.get_in_transaction(user, obfuscated_sample)
                            sample_id = int(syssample_id)

                            # Get the value of the info
                            value = ""
                            if field_type == "string":
                                sysval = test.get_in_transaction(user, field_value)
                                if sysval is None:
                                    value = field_value
                                else:
                                    _, syssample_id = sysval
                                    value = syssample_id

                            else:
                                with field_value.stream as f:
                                    value = f.read()

                            sm.logger.info(f"([sample={sample_id}, system={system}] - {name_col}: {value})")
                            _ = test.model.create(
                                user_id=user.id,
                                intro=intro_step,
                                step_idx=cur_step + 1,
                                sample_id=sample_id,
                                info_type=name_col,
                                info_value=value,
                                commit=False,
                            )

            except Exception as e:
                raise (e)
                test.delete_transaction(user)
                return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

        # Commit the results and clean the transations of the user
        commit_all()
        test.delete_transaction(user)

        if skip_after_n_step is not None:
            if (cur_step + 1) % skip_after_n_step == 0:
                next_urls: dict[str, str] = stage.next_local_urls
                if len(next_urls.keys()) > 1:
                    raise Exception("Only, one following step is supported here, configuration seems bogus")
                stage_name = list(next_urls.keys())[0]
                return redirect(next_urls[stage_name])

        return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

    @sm.route("/monitor", methods=["POST"])
    @sm.valid_connection_required
    def monitor() -> Response:
        """Saving routine of the test

        This method is called after the submission of the form
        implemented in the template associated to the step of the
        test.
        This method does:
          0. requiring a exclusive access to the db to avoid concurrency issue
          1. parsing the values of each *field* recorded by the method =save_field_name*
          2. filling the database *and creating new columns if necessary!*

        """
        # NOTE: to debug in case some is wrong, just run the following line
        stage = sm.current_stage
        test = test_manager.get(stage.name)  # TestManager(stage).get(stage.name)
        user = sm.auth_provider.user

        # Log the request form for debugging purposes
        sm.logger.debug("#### The request form ####")
        sm.logger.debug(request.json)  # TODO: prettify
        sm.logger.debug("#### <END>The request form ####")

        # Initialize the number of intro steps
        nb_step_intro = int(stage.get("nb_step_intro"))
        cur_step: int = test.nb_steps_complete_by(user)

        # Validate is the current step is an introduction step
        intro_step = False
        if nb_step_intro > cur_step:
            intro_step = True

        # Lock DB so we can update it (NOTE SLM: not sure that's what this does!)
        if not test.has_transaction(user):
            abort(408)

        try:
            # Get the JSON data sent in the POST request
            # FIXME: deal with multiple samples would be great
            monitoring_info = request.json
            obfuscated_sample_id = monitoring_info.get("sample_id")
            info_type = monitoring_info.get("info_type")
            info_value = monitoring_info.get("info_value")

            # TODO: should be generalised
            if isinstance(info_value, str) and info_value.startswith("sampleid:"):
                _, syssample_id = test.get_in_transaction(user, info_value.replace("sampleid:", ""))
                info_value = int(syssample_id)
            elif isinstance(info_value, list):
                values = []
                for cur_value in info_value:
                    if isinstance(cur_value, str) and cur_value.startswith("sampleid:"):
                        _, syssample_id = test.get_in_transaction(user, cur_value.replace("sampleid:", ""))
                        cur_value = int(syssample_id)
                    values.append(cur_value)
                info_value = values

            # Retrieve the sample information
            system, syssample_id = test.get_in_transaction(user, obfuscated_sample_id)
            sample_id = int(syssample_id)

            # Insert info in the model
            sm.logger.info(f"([sample={sample_id}, system={system}] - {info_type}: {info_value})")
            _ = test.model.create(
                user_id=user.id,
                intro=intro_step,
                step_idx=cur_step,
                sample_id=sample_id,
                info_type=info_type,
                info_value=info_value,
                commit=False,
            )
        except Exception as e:
            sm.logger.error(e)
            return Response(status=500)

        # Commit the results and clean the transations of the user
        commit_all()

        return Response(status=204)
