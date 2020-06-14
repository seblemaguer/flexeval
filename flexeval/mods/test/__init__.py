# coding: utf8
import random
from math import ceil
from flask import current_app, request, abort

from flexeval.core import StageModule,Stage, Config
from flexeval.utils import redirect
from flexeval.database import db,commit_all

from .src import TestManager

class TestsAlternateError(Exception):
    pass

class MalformationError(TestsAlternateError):
    def __init__(self,message):
        self.message = message

with StageModule(__name__) as sm:

    @sm.route("/", methods = ['GET'])
    @sm.connection_required
    def main():

        stage = sm.current_stage
        max_steps = int(stage.get("nb_steps"))
        nb_step_intro = stage.get("nb_step_intro")

        transaction_timeout_seconds = stage.get("transaction_timeout_seconds")

        if nb_step_intro is None:
            nb_step_intro = 0

        test = TestManager().get(stage.name)

        if transaction_timeout_seconds is not None:
            test.set_timeout_for_transaction(int(transaction_timeout_seconds))

        user = sm.authProvider.user

        steps = test.nb_steps_complete_by(user)

        intro_step = False
        if nb_step_intro > steps:
            intro_step = True
        else:
            intro_step = False


        if(steps < max_steps):
            syssamples_for_this_step = test.get_step(user,is_intro_step=intro_step)

            def get_syssamples(*system_names):
                systems = []
                if(len(system_names) == 0):
                    for syssample in syssamples_for_this_step.values():
                        systems.append(syssample)
                else:
                    for name_system in system_names:
                        systems.append(syssamples_for_this_step[name_system])

                random.shuffle(systems)

                return systems

            def save_field_name(name,syssamples=get_syssamples()):
                name = name.replace(":","_")
                ID=""

                for syssample in syssamples:
                    ID = ID+":"+syssample.ID

                ID = "save:"+name+ID

                return ID

            # On change les valeurs max_steps et steps pour l'affichage sur la page web
            if intro_step :
                max_steps = nb_step_intro
                steps = steps + 1
            else:
                max_steps = max_steps - nb_step_intro
                steps = steps + 1 - nb_step_intro

            return sm.render_template(template=stage.template,max_steps=max_steps,step=steps,intro_step=intro_step,syssamples=get_syssamples,field_name=save_field_name)
        else:
            return redirect(stage.local_url_next)

    @sm.route("/save", methods = ['POST'])
    @sm.connection_required
    def save():

        stage = sm.current_stage
        test = TestManager().get(stage.name)
        user = sm.authProvider.user
        skip_after_n_step = stage.get("skip_after_n_step")

        nb_step_intro = stage.get("nb_step_intro")
        steps = test.nb_steps_complete_by(user)

        intro_step = False
        if nb_step_intro > steps:
            intro_step = True

        if test.has_transaction(user):
            resp = test.testSampleModel.create(user_pseudo=user.pseudo,intro=intro_step,commit=False)
            try:
                for field_type, field_list in [("string",request.form), ("file",request.files)]:
                    for field_key in field_list.keys():
                        field_value = field_list[field_key]

                        if(field_key[:5] == "save:"):
                            field_key = field_key[5:]
                            (name_field,*idsyssamples) = field_key.split(":")

                            name_col = name_field
                            tmp_system_names = []

                            for idsyssample in idsyssamples:
                                (system_name,syssample_id) = test.get_in_transaction(user,idsyssample)
                                tmp_system_names.append(system_name)
                                #test.testSampleModel.addColumn(system_name,db.String)
                                sys = {system_name:syssample_id}

                                while test.systems[system_name][1] is not None:
                                    system_name = test.systems[system_name][1]
                                    syssample_id = test.get_in_transaction(user,"choice_for_systems")[system_name]._systemsample.id
                                    sys[system_name] = syssample_id
                                resp.update(commit=False,**sys)

                            tmp_system_names.sort()
                            for name_system in tmp_system_names:
                                name_col = name_col +"_"+name_system
                        else:
                            name_col = field_key

                        if field_type == "string":
                            test.testSampleModel.addColumn(name_col,db.String)
                            # On check si field_value n'est pas un lien vers un sysSample.
                            sysval = test.get_in_transaction(user,field_value)

                            if sysval is None:
                                resp.update(commit=False,**{name_col:field_value})
                            else:
                                (system_name,syssample_id) = sysval
                                resp.update(**{name_col:system_name})
                        else:
                            test.testSampleModel.addColumn(name_col,db.BLOB)

                            with field_value.stream as f:
                                resp.update(commit=False,**{name_col:f.read()})

            except Exception as e:
                test.delete_transaction(user)
                return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))

            commit_all()
            test.delete_transaction(user)

            if skip_after_n_step is not None:
                if (steps+1) % skip_after_n_step == 0:
                    return redirect(stage.local_url_next)

            return redirect(sm.url_for(sm.get_endpoint_for_local_rule("/")))
        else:
            abort(408)

with StageModule(__name__,subname="alternate") as sm_alternate:

    @sm_alternate.route("/", methods = ['GET'])
    @sm_alternate.connection_required
    def main():
        stage = sm_alternate.current_stage
        user = sm_alternate.authProvider.user
        nb_steps_before_alternate = stage.get("nb_steps_before_alternate")

        if "previous_stage" in stage.session:
            previous_stage = stage.session["previous_stage"]
        else:
            previous_stage = None

        stages_before_test = []
        tests = {}

        alternate_step = []
        alternate_max_step = []

        for alternate_stage_name in stage.get("stages"):
            alternate_stage = Stage(alternate_stage_name)
            alternate_stage.update("next",stage.name)

            Config().load_module(alternate_stage.mod_name)

            if alternate_stage.mod_name == sm.mod_rep:
                alternate_stage.update("skip_after_n_step",nb_steps_before_alternate)
                test = TestManager().get(alternate_stage_name)
                steps = test.nb_steps_complete_by(user)
                nb_steps = alternate_stage.get("nb_steps")

                alternate_max_step.append(ceil(nb_steps/nb_steps_before_alternate))
                is_end = False
                if(steps >= nb_steps):
                    is_end = True
                else:
                    alternate_step.append(ceil(steps/nb_steps_before_alternate))

                tests[alternate_stage_name] = (steps,stages_before_test,is_end)
                stages_before_test = []
            else:
                stages_before_test.append(alternate_stage_name)

        try:
            alternate_step = min(alternate_step)
            alternate_max_step = max(alternate_max_step)
            alternate_step = alternate_step + 1
        except Exception as e:
            alternate_max_step = max(alternate_max_step)
            alternate_step = alternate_max_step

        if len(stages_before_test) > 0:
            raise MalformationError("Issue with field:stages declared in structure.json; for stage:"+stage.name+". The last element of the list 'stages' need to be a stage of the type:"+sm.mod_rep+".")

        selected_test = None
        for test_name in tests.keys():
            steps = tests[test_name][0]
            is_active = not(steps % nb_steps_before_alternate == 0 )
            is_end = tests[test_name][2]
            if not(is_end):
                if is_active :
                    stage.session["previous_stage"] = test_name

                    n_stage = Stage(test_name)
                    n_stage.set_variable("alternate_step",alternate_step)
                    n_stage.set_variable("alternate_max_step",alternate_max_step)
                    n_stage.set_variable("alternate_nb_steps_per_iteration",nb_steps_before_alternate)
                    n_stage.set_variable("alternate_next_test",Stage(test_name).get_variable("subtitle",test_name))
                    return redirect(n_stage.local_url)
                else:
                    if selected_test is None:
                        selected_test = test_name
                    else:
                        steps_selected_test = tests[selected_test][0]
                        if( steps < steps_selected_test ):
                            selected_test = test_name

        if previous_stage in tests.keys():
            previous_stage = None
            stage.session["previous_stage"] = None

        if previous_stage is None:
            if not(selected_test is None):
                if len(tests[selected_test][1]) > 0:
                    stage.session["previous_stage"] = tests[selected_test][1][0]

                    n_stage = Stage(tests[selected_test][1][0])
                    n_stage.set_variable("alternate_step",alternate_step)
                    n_stage.set_variable("alternate_max_step",alternate_max_step)
                    n_stage.set_variable("alternate_nb_steps_per_iteration",nb_steps_before_alternate)
                    n_stage.set_variable("alternate_next_test",Stage(selected_test).get_variable("subtitle",selected_test))
                    return redirect(n_stage.local_url)

                else:
                    stage.session["previous_stage"] = selected_test

                    n_stage = Stage(selected_test)
                    n_stage.set_variable("alternate_step",alternate_step)
                    n_stage.set_variable("alternate_nb_steps_per_iteration",nb_steps_before_alternate)
                    n_stage.set_variable("alternate_max_step",alternate_max_step)
                    n_stage.set_variable("alternate_next_test",Stage(selected_test).get_variable("subtitle",selected_test))
                    return redirect(Stage(selected_test).local_url)
        else:
            next_stage = None
            for name_test in tests.keys():
                if previous_stage in tests[name_test][1]:
                    i_next_stage = tests[name_test][1].index(previous_stage) + 1
                    try:
                        next_stage = tests[name_test][1][i_next_stage]
                    except Exception as e:
                        next_stage = name_test
                    finally:
                        break;

            if next_stage is not None:
                stage.session["previous_stage"] = next_stage

                n_stage = Stage(next_stage)
                n_stage.set_variable("alternate_step",alternate_step)
                n_stage.set_variable("alternate_nb_steps_per_iteration",nb_steps_before_alternate)
                n_stage.set_variable("alternate_max_step",alternate_max_step)
                n_stage.set_variable("alternate_next_test",Stage(name_test).get_variable("subtitle",name_test))

                return redirect(n_stage.local_url)


        return redirect(stage.local_url_next)
