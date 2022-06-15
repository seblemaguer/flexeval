# coding: utf8
import random
from math import ceil
from flask import request, abort

import threading

from flexeval.core import StageModule, Stage, Config
from flexeval.utils import redirect
from flexeval.database import db, commit_all

from .src import TestManager

sem_test = threading.Semaphore()


class TestsAlternateError(Exception):
    pass


class MalformationError(TestsAlternateError):
    def __init__(self, message):
        self.message = message


with StageModule(__name__) as sm:

    @sm.route("/", methods=["GET"])
    @sm.valid_connection_required
    def main():
        """Entry point for the Test
        """

        # Get the current Stage
        stage = sm.current_stage

        # Get the type of test of the current stage
        test = TestManager().get(stage.name)

        # Load steps information
        max_steps = int(stage.get("nb_steps"))
        nb_step_intro = stage.get("nb_step_intro")
        if nb_step_intro is None:
            nb_step_intro = 0

        # Load systems per step information
        nb_systems_per_step = 1
        if stage.has("nb_systems_per_step"):
            nb_systems_per_step = int(stage.get("nb_systems_per_step"))
            if nb_systems_per_step <= 0:
                nb_systems_per_step = len(test.systems.keys())

        # Load transaction information
        transaction_timeout_seconds = stage.get("transaction_timeout_seconds")
        if transaction_timeout_seconds is not None:
            test.set_timeout_for_transaction(int(transaction_timeout_seconds))

        user = sm.authProvider.user

        cur_step = test.nb_steps_complete_by(user)
        if cur_step is None:
            cur_step = 0

        intro_step = False
        if nb_step_intro > cur_step:
            intro_step = True
        else:
            intro_step = False

        if cur_step < max_steps:

            # Get the step
            sem_test.acquire()
            syssamples_for_this_step = test.get_step(cur_step, user, nb_systems=nb_systems_per_step, is_intro_step=intro_step)
            sem_test.release()


            def get_syssamples(*system_names):
                systems = []
                if len(system_names) == 0:
                    for syssample in syssamples_for_this_step.values():
                        systems.append(syssample)
                else:
                    for name_system in system_names:
                        systems.append(syssamples_for_this_step[name_system])

                random.shuffle(systems)

                return systems

            def save_field_name(name, syssamples=get_syssamples(), record_name=None):
                name = name.replace(":", "_")

                # Make sure the record exist and get a real name if record name is None
                user = sm.authProvider.user
                record_name = test.get_record(user, record_name)
                
                # ID of the field
                ID = ":".join(["save",record_name,name]+[syssample.ID for syssample in syssamples])
                
                # Associate field to record
                test.add_field_to_record(user, ID, record_name)
                
                return ID
            
            def prepare_new_record(name=None):
                # Record new record for current step and current user
                user = sm.authProvider.user
                test.create_new_record(user, name)
                return name

            sm.logger.debug(f"Sample selected for this step is {get_syssamples()[0]}")

            # On change les valeurs max_steps et steps pour l'affichage sur la page web
            if intro_step:
                max_steps = nb_step_intro
                cur_step += 1
            else:
                max_steps = max_steps - nb_step_intro
                cur_step = cur_step +  1 - nb_step_intro

            return sm.render_template(
                template=stage.template,
                max_steps=max_steps,
                step=cur_step,
                intro_step=intro_step,
                syssamples=get_syssamples,
                field_name=save_field_name,
                new_record=prepare_new_record
            )
        else:
            return redirect(stage.local_url_next)

    @sm.route("/save", methods=["POST"])
    @sm.valid_connection_required
    def save():
        """Saving routine of the test
        """
        stage = sm.current_stage
        test = TestManager().get(stage.name)
        user = sm.authProvider.user
        skip_after_n_step = stage.get("skip_after_n_step")

        sm.logger.debug(request.form)
        # Initialize the number of intro steps
        nb_step_intro = stage.get("nb_step_intro")
        if nb_step_intro is None:
            nb_step_intro = 0

        # Get the current step
        cur_step = test.nb_steps_complete_by(user)
        if cur_step is None:
            cur_step = 0

        # Validate is the current step is an introduction step
        intro_step = False
        if nb_step_intro > cur_step:
            intro_step = True

        sem_test.acquire()
        # If there is no transaction, a timeout happened somewhere
        
        if not test.has_transaction(user):
            sem_test.release()
            abort(408)

        all_records = test.get_all_records(user)
        print(request.form)
        for (record_name, all_field_names) in all_records.items():
            resp = test.model.create(
                user_id=user.id, intro=intro_step, step_idx=cur_step+1, commit=False
            )
            try:
                for field_type, field_list in [
                    ("string", request.form),
                    ("file", request.files),
                ]:
                    for field_key in field_list.keys():
                        print("FIELD_KEY", field_key)
                        if field_key in all_field_names:
                            # Several values can be returned for one key (MultiDict) -> use d.get_list(key) instad d[key]
                            if len(field_list.getlist(field_key)) > 1:
                                field_value = str(field_list.getlist(field_key))
                            else:
                                field_value = field_list[field_key]

                            if field_key[:5] == "save:":
                                field_key = field_key[5:]
                                (record_name, field_name, *idsyssamples) = field_key.split(":")

                                name_col = field_name
                                tmp_system_names = []

                                for idsyssample in idsyssamples:
                                    (system_name, syssample_id) = test.get_in_transaction(
                                        user, idsyssample
                                    )
                                    tmp_system_names.append(system_name)
                                    sys = {system_name: syssample_id}

                                    resp.update(commit=False, **sys)

                                tmp_system_names.sort()
                                ###### GWENOLE: REMOVED BECAUSE I DON'T UNDERSTAND WHY IT IS USEFUL OR NEEDED
                                # for name_system in tmp_system_names:
                                    # name_col = name_col + "_" + name_system
                            else:
                                name_col = field_key

                            if field_type == "string":
                                test.model.addColumn(name_col, db.String)
                                # On check si field_value n'est pas un lien vers un sysSample.
                                sysval = test.get_in_transaction(user, field_value)

                                if sysval is None:
                                    resp.update(commit=False, **{name_col: field_value})
                                else:
                                    (system_name, syssample_id) = sysval
                                    resp.update(**{name_col: system_name})
                            else:
                                test.model.addColumn(name_col, db.BLOB)

                                with field_value.stream as f:
                                    resp.update(commit=False, **{name_col: f.read()})

            except Exception as e:
                raise(e)
                test.delete_transaction(user)
                sem_test.release()
                return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

        # Commit the results and clean the transations of the user
        commit_all()
        test.delete_transaction(user)
        sem_test.release()

        if skip_after_n_step is not None:
            if (cur_step + 1) % skip_after_n_step == 0:
                return redirect(stage.local_url_next)

        return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))
