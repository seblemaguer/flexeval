# coding: utf8
# license : CeCILL-C

# Import Libraries
import json
import os
import string
import random
import shutil

from flask import current_app, request,send_file
from sqlalchemy import MetaData, Table

from flexeval.core import AdminModule
from flexeval.utils import redirect,make_global_url,safe_make_rep
from flexeval.database import Model,db

with AdminModule(__name__) as am:

    safe_make_rep(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd")

    # Routes
    @am.route('/')
    @am.connection_required
    def panel():
        return am.render_template("index.tpl")

    @am.route('/flexeval.db')
    @am.connection_required
    def sqlite():
        return send_file(current_app.config["SQLALCHEMY_FILE"])


    @am.after_request
    def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    @am.route('/flexeval.zip')
    @am.connection_required
    def csv():
        repository_name = ''.join((random.choice(string.ascii_lowercase) for i in range(15)))
        safe_make_rep(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".bdd")


        for name_table in db.engine.table_names():
            table = Table(name_table, MetaData(), autoload=True, autoload_with=db.engine)

            cols = []
            primary_key = None
            content = ""
            headers = ""

            for col in table.columns:
                if col.primary_key:
                    primary_key = col.name
                cols.append(col)

                headers = headers+";"+col.name
            content = headers[1:] + "\n"

            q = db.session.query(table)

            for r in q.all():
                row=""
                for col in cols:

                    if isinstance(col.type,db.BLOB):
                        try:
                            file_content = getattr(r,col.name)
                            assert not(len(file_content) == 0)

                            with open(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".bdd/@table_"+name_table+"@"+col.name+"_"+str(getattr(r,primary_key))+".blob",'wb') as f:
                                f.write(file_content)
                            row = row+";@table_"+name_table+"@"+col.name+"_"+str(getattr(r,primary_key))+".blob"
                        except Exception as e:
                            row = row+";"
                    else:
                        row = row+";"+str(getattr(r,col.name))
                content = content + row[1:] + "\n"
            content = content[:len(content)-1]

            with open(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".bdd/"+name_table+".csv","w") as f:
                f.write(content)

        shutil.make_archive(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name,"zip",current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".bdd")
        shutil.rmtree(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".bdd")

        return send_file(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"]+"/export_bdd/"+repository_name+".zip")
