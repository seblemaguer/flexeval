from flask import Blueprint, render_template,url_for,request,redirect,session
from utils import db,config
from mods.questionnaire.model.QRResp import QRResp as mQRResp


bp = Blueprint('questionnaire', __name__,template_folder='templates',static_folder='../../static')

# Routes
@bp.route('/<name>', methods = ['GET'])
def get(name):

    oneAnswer = mQRResp.query.filter_by(name=name,user_id=session["user"]).first()
    if oneAnswer is None:
        return render_template(config["questionnaire"][name]["template"],qrname=name)
    else:
        return redirect(config["questionnaire"][name]["next"])

@bp.route('/<name>/send', methods = ['POST'])
def save(name):
    for question in request.form.keys():
        db.session.add(mQRResp(name,question,request.form[question],session["user"]))

    db.session.commit()


    return redirect(config["questionnaire"][name]["next"])
