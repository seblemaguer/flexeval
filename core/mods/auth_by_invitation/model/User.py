# Import Libraries
import random
import string

from core.utils import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True,nullable=False)
    token =  db.Column(db.String,unique=True,nullable=False)
    activated = db.Column(db.Boolean,nullable=False)

    def __init__(self,email):
        self.email = email
        self.token = ''.join((random.choice(string.ascii_lowercase) for i in range(20)))
        self.activated = False

    def activate(self):
        self.activated = True

    @property
    def json(self):

        return {"id":str(id),"email":str(self.email),"token":str(self.token),"activated":str(self.activated)}
