# Import Libraries
from core.utils import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True,nullable=False)

    def __init__(self,email):
        self.email = email

    @property
    def json(self):

        return {"id":str(id),"email":str(self.email)}
