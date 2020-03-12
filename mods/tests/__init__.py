from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config,NAME_REP_CONFIG,get_provider
from mods.tests.model import System as mSystem
from mods.tests.model import Sample as mSample
import random

bp = Blueprint('tests', __name__,template_folder=NAME_REP_CONFIG+'/templates',static_folder='../../assets')

# Routes
@bp.route('/<name>', methods = ['GET'])
def get(name):

    user_id = get_provider("auth").get()
    session["Test_"+str(name)] = False

    try:
        samples = mSample.Sample.query.filter_by(user_id=user_id,name_test=name).all()
    except Exception as e:
        samples = []

    choice = []
    for system in config["tests"][name]["systems"]:
        system = mSystem.System.get(NAME_REP_CONFIG+'/systems/'+system)

        nb_answer = 0
        select_question = None
        try:
            choice_per_system = []
            min_sample_per_syssample = 9999999999999999999

            for syssample in system.samples():
                cpt_sample_per_syssample = 0
                already_present_to_the_user = False
                for sample in syssample.samples:
                    if(sample.name_test == name):
                        if(sample.user_id == user_id):
                            already_present_to_the_user = True
                            if select_question is None:
                                select_question = sample.question

                            if sample.question == select_question:
                                nb_answer = nb_answer + 1
                                assert nb_answer < config["tests"][name]["#answer"]
                                if(nb_answer == config["tests"][name]["#answer"]):
                                    session["Test_"+str(name)] = True
                        else:
                            cpt_sample_per_syssample = cpt_sample_per_syssample + 1

                if not(already_present_to_the_user):
                    if(cpt_sample_per_syssample <= min_sample_per_syssample):
                        if cpt_sample_per_syssample < min_sample_per_syssample:
                            choice_per_system = [syssample]
                            min_sample_per_syssample = cpt_sample_per_syssample
                        else:
                            choice_per_system.append(syssample)

            choice.append(random.choice(choice_per_system))

        except Exception as e:
            return redirect(config["tests"][name]["next"])

        if len(choice) == 0:
            return redirect(config["tests"][name]["next"])

    random.shuffle(choice)
    return render_template(config["tests"][name]["template"],name=name,systems=choice)

@bp.route('/<name>/send', methods = ['POST'])
def save(name):
    user_id = get_provider("auth").get()

    if("Test_"+str(name) in session):

        for key in request.form.keys():
            rtn = mSystem.SysSample.get_save_field(key)
            if not(rtn is None):
                question = rtn[0]
                answer = request.form[key]
                syssample_id = rtn[1]

                sample = mSample.Sample(question,answer,name,user_id)
                syssample = mSystem.SysSample.query.filter_by(id=syssample_id).first()
                db.session.add(sample)
                syssample.samples.append(sample)
        db.session.commit()

    if session["Test_"+str(name)] == True:
        return redirect(config["tests"][name]["next"])
    else:
        return redirect("../"+str(name))
