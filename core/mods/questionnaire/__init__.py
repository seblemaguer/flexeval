# Import Libraries
from flask import Blueprint, render_template,request,redirect,session

from core.utils import db,config,get_provider
from core.mods.questionnaire.model.QRResp import QRResp as mQRResp

bp = Blueprint('questionnaire', __name__)

# Routes
@bp.route('/<name>', methods = ['GET'])
def get(name):

    oneAnswer = mQRResp.query.filter_by(name=name,user=get_provider("auth").get()).first()
    if oneAnswer is None:

        _parameters = None
        if "template:parameters" in config["stages"][name]:
            _parameters=config["stages"][name]["template:parameters"]

        return render_template(config["stages"][name]["template"],userprov=get_provider("auth"),qrname=name,parameters=_parameters)
    else:
        return redirect(config["stages"][name]["next"])

@bp.route('/<name>/send', methods = ['POST'])
def save(name):

    for (type, keys) in [("form",request.form.keys()),("file",request.files.keys())]:
        for key in keys:
            responseFORM = None
            responseFILE = None

            if type == "form":
                responseFORM = request.form[key]
            else:
                responseFILE = request.files[key]

            db.session.add(mQRResp(name,key,responseFORM=responseFORM,responseFILE=responseFILE))

    db.session.commit()


    return redirect(config["stages"][name]["next"])
