from sqlalchemy import orm
from utils import db

class QRResp(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    question = db.Column(db.String,nullable=False)
    responseSTRING = db.Column(db.String,nullable=True)
    responseBLOB = db.Column(db.BLOB)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self,name,question,userid,responseFORM=None,responseFILE=None):
        self.name = name
        self.question = question
        self.user_id = userid

        self.set_response_STRING(responseFORM)
        self.set_response_BLOB(responseFILE)


    def set_response_STRING(self,val):
        if not(val is None):
            self.responseSTRING = str(val)

    def set_response_BLOB(self,val):
        if not(val is None):
            try:
                with val.stream as f:
                    self.responseBLOB = f.read()
            except Exception as e:
                self.responseBLOB = None
