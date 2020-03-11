from sqlalchemy import orm
from utils import db

class QRResp(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    question = db.Column(db.String,nullable=False)
    response = db.Column(db.String,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self,name,question,response,userid):
        self.name = name
        self.question = question
        self.response = response
        self.user_id = userid
   
