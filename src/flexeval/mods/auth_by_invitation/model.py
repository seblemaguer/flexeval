import random
import string

from flexeval.core.stage import StageModuleUser
from flexeval.database import Column, db


class InvitedUser(StageModuleUser):
    token = Column(db.String, unique=True, nullable=False)
    active = Column(db.Boolean, nullable=False)
    LEN_TOKEN = 20

    def __init__(self, email: str):
        super().__init__()
        self.id = email
        self.token = "".join((random.choice(string.ascii_lowercase) for _ in range(InvitedUser.LEN_TOKEN)))
        self.active = False
