# coding: utf8
from datetime import datetime

from flexeval.database import Model,relationship, Column, ForeignKey, db, declared_attr
from flexeval.core import StageModule

usermodel = StageModule.get_UserModel()

class TestSample(Model):

    __abstract__ = True

    id = Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    intro = db.Column(db.Boolean, nullable=False)

    def __init__(self,*args,**kwargs):
        self.intro = False
        super().__init__(*args,**kwargs)
        self.date = datetime.now()

    @declared_attr
    def user_pseudo(cls):
        return Column(db.String, ForeignKey(usermodel.__tablename__+'.pseudo'))

    @declared_attr
    def user(cls):
        return relationship(usermodel.__name__,
            primaryjoin=usermodel.__name__+".pseudo==%s.user_pseudo" % cls.__name__
        )
