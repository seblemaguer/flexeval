# coding: utf8
# license : CeCILL-C

# Import Libraries
import json
import os
import string
import random
import shutil

from flask import current_app, request, send_file
from sqlalchemy import MetaData, Table

from flexeval.core import AdminModule
from flexeval.utils import redirect, make_global_url, safe_make_rep
from flexeval.database import Model, db

with AdminModule(__name__) as am:
    safe_make_rep(current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"] + "/export_bdd")

    # Routes
    @am.route("/")
    @am.valid_connection_required
    def panel():
        return am.render_template("index.tpl")

    @am.route("/flexeval.db")
    @am.valid_connection_required
    def sqlite():
        return send_file(current_app.config["SQLALCHEMY_FILE"])

    @am.after_request
    def set_response_headers(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @am.route("/flexeval.zip")
    @am.valid_connection_required
    def csv():
        repository_name = "".join((random.choice(string.ascii_lowercase) for i in range(15)))
        root_base_file = current_app.config["FLEXEVAL_INSTANCE_TMP_DIR"] + "/export_bdd/" + repository_name

        safe_make_rep(root_base_file + ".bdd")

        for name_table in db.engine.table_names():
            table = Table(name_table, MetaData(), autoload=True, autoload_with=db.engine)

            # Generate header
            headers = ""
            cols = []
            primary_key = None
            for col in table.columns:
                if col.primary_key:
                    primary_key = col.name
                cols.append(col)
                headers = headers + ";" + col.name

            content = ""
            content = headers[1:] + "\n"

            # Fill the content
            q = db.session.query(table)
            for r in q.all():
                row = ""
                for col in cols:
                    if isinstance(col.type, db.BLOB):
                        try:
                            file_content = getattr(r, col.name)
                            assert not (len(file_content) == 0)

                            table_fn = (
                                f"{root_base_file}.bdd/@table_{name_table}@{col.name}_{getattr(r,primary_key)}.blob"
                            )
                            with open(table_fn, "wb") as f:
                                f.write(file_content)
                            row += f";@table_{name_table}@{col.name}_{getattr(r,primary_key)}.blob"
                        except Exception as e:
                            row += ";"
                    else:
                        row = row + ";" + str(getattr(r, col.name))
                content = content + row[1:] + "\n"
            content = content[: len(content) - 1]

            table_fn = f"{root_base_file}.bdd/{name_table}.csv"
            with open(table_fn, "w") as f:
                f.write(content)

        # Generate the archive and return it!
        shutil.make_archive("flexeval", "zip", f"{root_base_file}.bdd")
        shutil.rmtree(f"{root_base_file}.bdd")

        return send_file("../flexeval.zip")  # FIXME: why should I have to go to the parent directory?
