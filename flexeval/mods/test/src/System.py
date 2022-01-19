# coding: utf8
import csv

from flask import current_app
from sqlalchemy import asc

from flexeval.utils import AppSingleton
from flexeval.database import db, commit_all

from flexeval.mods.test.model import SampleModel


class SystemError(Exception):
    def __init__(self, message):
        self.message = message


class SystemFileNotFound(SystemError):
    pass


class SystemManager(metaclass=AppSingleton):
    def __init__(self):
        self.register = {}

    def get(self, name, delimiter=",", max_samples=-1):
        if not (name in self.register):
            self.register[name] = System(name, delimiter, max_samples)

        return self.register[name]


class System:
    def __init__(self, name, delimiter=",", max_samples=-1):

        if name[0] == "/":
            name = name[1:]

        self.name = name
        source_file = (
            current_app.config["FLEXEVAL_INSTANCE_DIR"]
            + "/systems/"
            + self.name
            + ".csv"
        )

        try:
            reader = csv.DictReader(open(source_file, encoding="utf-8"), delimiter=delimiter)
        except Exception as e:
            raise SystemFileNotFound(
                source_file + " doesn't exist. Fix test.json or add the system's file."
            )

        self.cols_name = reader.fieldnames

        # On crée ou réhydrate la classe SampleModel
        # Il est important de faire cela avant de créer les instances de SampleModel
        # Sinon seulement les columns définies de base dans SampleModel seront disponibles.
        for col_name in self.cols_name:
            SampleModel.addColumn(col_name, db.String)

        if max_samples < 0:
            max_samples = len(reader)

        if len(self.system_samples) == 0:

            for line_id, line in enumerate(reader):

                if line_id > max_samples:
                    break

                vars = {"system": self.name, "line_id": line_id}

                try:
                    for col_name in self.cols_name:
                        vars[col_name] = line[col_name]

                    SampleModel.create(commit=False, **vars)

                except Exception as e:
                    raise SystemError(
                        "Issue to read the line "
                        + str(line_id)
                        + " of the file:"
                        + source_file
                    )

            commit_all()

    @property
    def system_samples(self):

        return (
            SampleModel.query.filter(SampleModel.system == self.name)
            .order_by(SampleModel.line_id.asc())
            .all()
        )
