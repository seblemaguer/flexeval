from sqlalchemy import orm
from utils import db, config, get_provider
import csv

class SystemSample(db.Model):
    __tablename__ = 'systemsample'

    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer,nullable=False)
    line_value = db.Column(db.JSON,nullable=False)
    source = db.Column(db.String,nullable=False)

    def __init__(self,line_id,line_value,source):

        self.line_id = line_id
        self.line_value = line_value
        self.source = source
