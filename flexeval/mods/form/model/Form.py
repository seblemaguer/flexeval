# coding: utf8
# license : CeCILL-C

# Import Libraries
from flexeval.core import StageModule
from flexeval.database import Model,relationship, Column, ForeignKey, db, declared_attr

userModel = StageModule.get_UserModel()

class Form(Model):

    __abstract__ = True

    id = Column(db.Integer, primary_key=True)

    @declared_attr
    def user_pseudo(cls):
        return Column(db.String, ForeignKey(userModel.__tablename__+'.pseudo'))
