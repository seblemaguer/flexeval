from sqlalchemy import orm
from utils import db, config, get_provider
import csv

class Sample(db.Model):
    __tablename__ = 'sample'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    system_sample_id = db.Column(db.Integer)

    name_test = db.Column(db.String, nullable=False)
    name_system = db.Column(db.String, nullable=False)
    step = db.Column(db.Integer, nullable=False)

    question = db.Column(db.String,nullable=False)
    answerSTRING = db.Column(db.String,nullable=True)
    answerBLOB = db.Column(db.BLOB)

    def __init__(self,system_sample_id,name_test,name_system,step,question,answerSTRING=None,answerBLOB=None):

        self.user_id = get_provider("auth").get()

        self.system_sample_id = system_sample_id
        self.name_test = name_test
        self.name_system = name_system

        self.step = step

        self.question = question
        self.set_answer_STRING(answerSTRING)
        self.set_answer_BLOB(answerBLOB)

    def set_answer_STRING(self,val):
        if not(val is None):
            self.answerSTRING = str(val)

    def set_answer_BLOB(self,val):
        if not(val is None):
            try:
                with val.stream as f:
                    self.answerBLOB = f.read()
            except Exception as e:
                self.answerBLOB = None
