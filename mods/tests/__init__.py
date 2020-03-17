from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config,NAME_REP_CONFIG,get_provider,instance_data
from mods.tests.src.Test import Test
from mods.tests.src.System import SystemTemplate
from mods.tests.model.Sample import Sample
import random

bp = Blueprint('tests', __name__,template_folder=NAME_REP_CONFIG+'/templates')

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
            session["tests"][name][system_sample[name_system].id] = {"name_system":name_system}

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

        return render_template(config["stages"][name]["template"],name=name,systems=systems)

@bp.route('/<name>/send', methods = ['POST'])
def save(name):

    test = Test(name)

    unique_system_answer = test.unique_system_answer()

    if(unique_system_answer >= test.nb_answers_max):
        return redirect(config["stages"][name]["next"])
    else:

        for (type, keys) in [("form",request.form.keys()),("file",request.files.keys())]:
            for key in keys:

                rtn = SystemTemplate.get_save_field(key)

                if not(rtn is None):
                    question = rtn[0]

                    answerFORM = None
                    answerFILE = None

                    if type == "form":
                        answerFORM = request.form[key]
                    else:
                        answerFILE = request.files[key]

                    system_sample_id = rtn[1]
                    name_system = session["tests"][name][system_sample_id]["name_system"]
                    step = unique_system_answer

                    sample = Sample(system_sample_id,name,name_system,step,question,answerSTRING=answerFORM,answerBLOB=answerFILE)
                    db.session.add(sample)

        db.session.commit()
        del session["tests"]

        return redirect("../"+name)
