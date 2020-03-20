# Import Libraries
from core.utils import db, get_provider

class QRResp(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    question = db.Column(db.String,nullable=False)
    responseSTRING = db.Column(db.String,nullable=True)
    responseBLOB = db.Column(db.BLOB,nullable=True)
    user = db.Column(db.String, nullable=False)

    def __init__(self,name,question,responseFORM=None,responseFILE=None):
        self.name = name
        self.question = question
        self.user = get_provider("auth").get()

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
