# coding: utf8
from datetime import datetime

from flexeval.database import Model,relationship, Column, ForeignKey, db, declared_attr
from flexeval.core import StageModule

usermodel = StageModule.get_UserModel()

class SampleModel(Model):

    __tablename__ = "Sample"

    id = Column(db.Integer, primary_key=True)
    system = Column(db.String, nullable=False)
    line_id = Column(db.Integer,nullable=False)


class TestModel(Model):

    __abstract__ = True

    id = Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    step_idx = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Boolean, nullable=False)

    def __init__(self,*args,**kwargs):
        self.intro = False
        super().__init__(*args,**kwargs)
        self.date = datetime.now()

    @declared_attr
    def user_id(cls):
        return Column(db.String, ForeignKey(usermodel.__tablename__+'.id'))

    @declared_attr
    def user(cls):
        return relationship(usermodel.__name__,
            primaryjoin=usermodel.__name__+".id==%s.user_id" % cls.__name__
        )
