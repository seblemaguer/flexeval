# Import Libraries
import random
import json

from flask import Blueprint, render_template,request,redirect,session

from core.utils import db,config,NAME_REP_CONFIG,assets
from core.mods.tests.src.Test import Test
from core.mods.tests.src.System import SystemTemplate
from core.mods.tests.model.Sample import Sample

bp = Blueprint('tests', __name__)
tests_data = None

with open(NAME_REP_CONFIG+'/tests.json') as tests_data_json:
    tests_data = json.load(tests_data_json)

# Routes
@bp.route('/<name>', methods = ['GET'])
def get(name):

    test = Test(name)

    unique_system_answer = test.unique_system_answer()

    if(unique_system_answer >= test.nb_answers_max):
        return redirect(config["stages"][name]["next"])
    else:
        session["tests"] = {name:{}}
        system_sample = test.get_system_sample()

        for name_system in system_sample.keys():
            session["tests"][name][str(system_sample[name_system].id)] = {"name_system":name_system}

        def systems(*args):
            systems = []

            if(len(args) == 0):
                for name_system in system_sample.keys():
                    systems.append(SystemTemplate(name_system,system_sample[name_system]))
            else:
                for name_system in args:
                    systems.append(SystemTemplate(name_system,system_sample[name_system]))

            random.shuffle(systems)
            return systems

        return render_template(config["stages"][name]["template"],name=name,systems=systems,save_field=SystemTemplate.save_field,obfuscate_assets=assets.obfuscate)

@bp.route('/<name>/send', methods = ['POST'])
def save(name):

    test = Test(name)

    unique_system_answer = test.unique_system_answer()

    if(unique_system_answer >= test.nb_answers_max):
        return redirect(config["stages"][name]["next"])
    else:
        step = unique_system_answer
        for (type, keys) in [("form",request.form.keys()),("file",request.files.keys())]:
            for key in keys:

                rtn = SystemTemplate.get_save_field(key)

                if not(rtn is None):
                    (question,systems) = rtn

                    answerFORM = None
                    answerFILE = None

                    if type == "form":
                        answerFORM = request.form[key]
                        rtn = SystemTemplate.get_name(answerFORM)
                        if not(rtn is None):
                            answerFORM = rtn
                    else:
                        answerFILE = request.files[key]

                    for system in systems:
                        sample = Sample(system["systemsample_id"],name,system["name_system"],step,question,answerSTRING=answerFORM,answerBLOB=answerFILE)
                        db.session.add(sample)

        db.session.commit()
        del session["tests"]

        return redirect("../"+name)
