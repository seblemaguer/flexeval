# Import Libraries
import json
import os
import string
import random
import shutil

from flask import Blueprint,request, send_from_directory, abort, current_app, session

import core.utils as utils

# Config
TITLE = "Download BDD"
DESCRIPTION = "Download the database in CSV or SQLite format."

# Initialize
bp = Blueprint('export', __name__)
os.makedirs(utils.NAME_REP_CONFIG+"/.tmp/export_bdd")

# Routes
@bp.route('/')
def panel():
    return utils.render_template("admin/export/panel.tpl")

@bp.route('/bdd.zip')
def csv():

    repository_name = ''.join((random.choice(string.ascii_lowercase) for i in range(15)))

    os.makedirs(utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name)

    #https://stackoverflow.com/questions/26514823/get-all-models-from-flask-sqlalchemy-db
    db = current_app.extensions['sqlalchemy'].db

    lclasses = [cls for cls in db.Model._decl_class_registry.values() if isinstance(cls, type) and issubclass(cls, db.Model)]

    for lclass in lclasses:

        cols = []
        primary_key = None
        name_table = str(lclass.__table__)
        content = ""
        headers = ""

        for col in lclass.__table__.columns:
            if col.primary_key:
                primary_key = col.name
            cols.append(col)

            headers = headers+";"+col.name
        content = headers[1:] + "\n"

        q = utils.db.session.query(lclass)

        for r in q.all():
            row=""
            for col in cols:

                if isinstance(col.type,utils.db.BLOB):
                    try:
                        file_content = getattr(r,col.name)
                        assert not(len(file_content) == 0)

                        with open(utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name+"/@table_"+name_table+"@"+col.name+"_"+str(getattr(r,primary_key))+".blob",'wb') as f:
                            f.write(file_content)
                        row = row+";@table_"+name_table+"@"+col.name+"_"+str(getattr(r,primary_key))+".blob"
                    except Exception as e:
                        row = row+";"
                else:
                    row = row+";"+str(getattr(r,col.name))
            content = content + row[1:] + "\n"
        content = content[:len(content)-1]

        with open(utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name+"/"+name_table+".csv","w") as f:
            f.write(content)

    shutil.make_archive(utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name,"zip",utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name)
    shutil.rmtree(utils.NAME_REP_CONFIG+"/.tmp/export_bdd/"+repository_name)

    return send_from_directory(utils.NAME_REP_CONFIG+"/.tmp/export_bdd",repository_name+".zip")

@bp.route('/bdd.sqlite')
def sqlite():

    return send_from_directory(utils.NAME_REP_CONFIG,"bdd_sqlite.db")
