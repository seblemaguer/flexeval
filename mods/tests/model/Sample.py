from sqlalchemy import orm
from utils import db, config
import csv

class Sample(db.Model):
    __tablename__ = 'sample'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    syssample_id = db.Column(db.Integer, db.ForeignKey('syssample.id'))
    name_test = db.Column(db.String, nullable=False)

    question = db.Column(db.String,nullable=False)
    answer = db.Column(db.String,nullable=False)

    def __init__(self,question,answer,name_test,user_id):
        self.name_test = name_test
        self.user_id = user_id

        self.question = question
        self.answer = answer
