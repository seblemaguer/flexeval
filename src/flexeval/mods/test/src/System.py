# coding: utf8
from typing import Sequence, Any
import csv

from flask import current_app

from flexeval.utils import AppSingleton
from flexeval.database import db, commit_all

from flexeval.mods.test.model import SampleModel


class SystemError(Exception):
    def __init__(self, message: str):
        self.message = message


class SystemFileNotFound(SystemError):
    pass


class System:
    def __init__(self, name: str, data: str, delimiter: str = ",", max_samples: int = -1):
        if name[0] == "/":
            name = name[1:]

        self.name = name
        source_file: str = current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/systems/" + data

        try:
            reader = csv.DictReader(open(source_file, encoding="utf-8"), delimiter=delimiter)
        except Exception as e:
            raise SystemFileNotFound(f"{source_file} doesn't exist. Fix test.json or add the system's file: {e}")

        assert reader.fieldnames is not None
        self._col_names: Sequence[str] = reader.fieldnames

        # Dynamically create the columns needed to populate all the information related to the current sample
        for col_name in self._col_names:
            SampleModel.addColumn(col_name, db.String)

        if max_samples < 0:
            max_samples = len(list(csv.DictReader(open(source_file, encoding="utf-8"), delimiter=delimiter)))

        if len(self.system_samples) == 0:
            for line_id, line in enumerate(reader):
                if line_id >= max_samples:
                    break

                vars = {"system": self.name, "line_id": line_id}

                try:
                    for col_name in self._col_names:
                        vars[col_name] = line[col_name]

                    SampleModel.create(commit=False, **vars)

                except Exception as e:
                    raise SystemError(f'Issue to read the line {line_id} of the file "{source_file}": {e}')

            commit_all()

    @property
    def system_samples(self) -> list[Any]:
        return SampleModel.query.filter(SampleModel.system == self.name).order_by(SampleModel.line_id.asc()).all()


class SystemManager(metaclass=AppSingleton):
    def __init__(self):
        self.register: dict[str, System] = {}

    def insert(self, name: str, data: str, delimiter: str = ",", max_samples: int = -1):
        self.register[name] = System(name, data, delimiter, max_samples)
        return self.register[name]

    def get(self, name: str) -> System:
        return self.register[name]
