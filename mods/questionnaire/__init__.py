from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config,NAME_REP_CONFIG,get_provider
from mods.questionnaire.model.QRResp import QRResp as mQRResp


bp = Blueprint('questionnaire', __name__)

# Routes
@bp.route('/<name>', methods = ['GET'])
def get(name):

    oneAnswer = mQRResp.query.filter_by(name=name,user=get_provider("auth").get()).first()
    if oneAnswer is None:
        return render_template(config["stages"][name]["template"],qrname=name)
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
