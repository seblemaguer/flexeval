# coding: utf8
# license : CeCILL-C

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

session_manager = Session()
db = SQLAlchemy()
