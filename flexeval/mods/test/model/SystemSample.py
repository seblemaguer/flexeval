# coding: utf8
from flexeval.database import Model, Column, db

class SystemSample(Model):

    __tablename__ = "SystemSample"

    id = Column(db.Integer, primary_key=True)
    system = Column(db.String, nullable=False)
    line_id = Column(db.Integer,nullable=False)
