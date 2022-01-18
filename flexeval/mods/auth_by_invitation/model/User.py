# coding: utf8
# license : CeCILL-C

import random
import string

from flexeval.core import UserModel
from flexeval.database import Column,db

class User(UserModel):

    token =  Column(db.String,unique=True,nullable=False)
    active = Column(db.Boolean,nullable=False)

    def __init__(self,email):

        self.token = ''.join((random.choice(string.ascii_lowercase) for i in range(20)))
        self.active = False
        self.id = email
