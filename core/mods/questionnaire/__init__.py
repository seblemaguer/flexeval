# Import Libraries
from flask import Blueprint,request,redirect,session, abort

from core.utils import db,config,get_provider,render_template
from core.mods.questionnaire.model.QRResp import QRResp as mQRResp
from core.src.Module import StageModule

with StageModule('questionnaire', __name__) as bp:

    # Routes
    @bp.route('/<name>', methods = ['GET'])
    def get(name):

        if(name not in config["stages"]):
            abort(404)

        oneAnswer = mQRResp.query.filter_by(name=name,user=get_provider("auth").get()).first()
        if oneAnswer is None:
            return render_template(config["stages"][name]["template"],stage_name=name)
        else:
            return redirect(config["stages"][name]["next"])

    @bp.route('/<name>/send', methods = ['POST'])
    def save(name):

        if(name not in config["stages"]):
            abort(404)

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
