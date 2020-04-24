# coding: utf8
import csv

from flask import current_app
from sqlalchemy import asc

from flexeval.utils import AppSingleton
from flexeval.database import db,commit_all

from flexeval.mods.test.model import SystemSample

class SystemError(Exception):

    def __init__(self,message):
        self.message = message

class SystemFileNotFound(SystemError):
    pass


class SystemManager(metaclass=AppSingleton):

    def __init__(self):
        self.register={}

    def get(self,name):
        if not(name in self.register):
            self.register[name] = System(name)

        return self.register[name]

class System():

    def __init__(self,name):

        if name[0] == "/":
            name = name[1:]

        self.name = name
        source_file = current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/systems/"+self.name+".csv"

        try:
            reader = csv.DictReader(open(source_file,encoding='utf-8'))
        except Exception as e:
            raise SystemFileNotFound(source_file+" doesn't exist. Fix test.json or add the system's file.")

        self.cols_name = reader.fieldnames

        # On crée ou réhydrate la classe SystemSample
        # Il est important de faire cela avant de créer les instances de SystemSample
        # Sinon seulement les columns définies de base dans SystemSample seront disponibles.
        for col_name in self.cols_name:
            SystemSample.addColumn(col_name,db.String)

        if len(self.system_samples) == 0:

            for line_id, line in enumerate(reader):

                vars={"system":self.name,"line_id":line_id}

                try:
                    for col_name in self.cols_name:
                        vars[col_name]=line[col_name]

                    SystemSample.create(commit=False,**vars)

                except Exception as e:
                    raise SystemError("Issue to read the line "+str(line_id)+" of the file:"+source_file)

            commit_all()

    @property
    def system_samples(self):

        return SystemSample.query.filter(SystemSample.system == self.name).order_by(SystemSample.line_id.asc()).all()
