# coding: utf8

from typing import Dict, List

# Global/system
import os
from pathlib import Path
import string
import logging

# Yaml
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Data type
import base64
import mimetypes
import random
from datetime import datetime, timedelta

# Flask
from flask import current_app

# Flexeval
from flexeval.utils import AppSingleton
from flexeval.core import StageModule, UserModel
from flexeval.database import ForeignKey, ModelFactory, db
from flexeval.mods.test.model import TestModel, SampleModel

# Current package
from .System import SystemManager
from .selection_strategy import FirstServerSelection

TEST_CONFIGURATION_BASENAME = "tests"
DEFAULT_CSV_DELIMITER = ","


class SampleModelTemplate:
    def __init__(self, id, system_name, systemsample):
        self._system = SystemManager().get(systemsample.system)
        self._systemsample = systemsample
        self.system_name = system_name
        self._ID = id

    @property
    def ID(self):
        return self._ID

    def get(self, name=None, num=None):
        if num is not None:
            name = self._system.cols_name[num]

        if name is None:
            return (None, None)
        else:

            mime = "text"
            value = getattr(self._systemsample, name)

            file_path = value

            if not (file_path[0] == "/"):
                file_path = "/" + file_path

            if Path(
                current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/systems" + file_path
            ).is_file():
                mime, _ = mimetypes.guess_type(
                    current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/systems" + file_path
                )

                with open(
                    current_app.config["FLEXEVAL_INSTANCE_DIR"]
                    + "/systems"
                    + file_path,
                    "rb",
                ) as f:
                    data64 = base64.b64encode(f.read()).decode("utf-8")
                    value = "data:%s;base64,%s" % (mime, data64)
                mime = mime.split("/")[0]

            return (value, mime)


class TestError(Exception):
    def __init__(self, message):
        self.message = message


class MalformationError(TestError):
    pass


class TestManager(metaclass=AppSingleton):
    def __init__(self):
        self.register = {}
        with open(
            os.path.join(
                current_app.config["FLEXEVAL_INSTANCE_DIR"],
                "%s.yaml" % TEST_CONFIGURATION_BASENAME,
            ),
            encoding="utf-8",
        ) as config_stream:
            self.config = load(config_stream, Loader=Loader)

    def get(self, name):
        if not (name in self.register):
            try:
                config = self.config[name]
            except Exception as e:
                raise MalformationError(
                    "Test "
                    + name
                    + " not found in %s.yaml." % TEST_CONFIGURATION_BASENAME
                )
            self.register[name] = Test(name, config)

        return self.register[name]

class TransactionalObject:
    def __init__(self):
        self.transactions = {}
        self.time_out_seconds = 3600

    def set_timeout_for_transaction(self, timeout):
        self.time_out_seconds = timeout

    def delete_transaction(self, user):
        del self.transactions[user.id]

    def create_transaction(self, user):
        self.transactions[user.id] = {"date": datetime.now()}

    def get_transactions(self):

        transactions = []
        to_del = []

        for key_transaction in self.transactions.keys():
            transaction = self.transactions[key_transaction]

            if (self.time_out_seconds is not None) and (
                transaction["date"] + timedelta(seconds=self.time_out_seconds)
                < datetime.now()
            ):
                to_del.append(key_transaction)
            else:
                transactions.append(transaction)

        for transaction_key_to_del in to_del:
            del self.transactions[transaction_key_to_del]

        return transactions

    def has_transaction(self, user):
        return user.id in self.transactions

    def get_transaction(self, user):
        return self.transactions[user.id]

    def set_in_transaction(self, user, name, obj):
        self.transactions[user.id][name] = obj

    def get_in_transaction(self, user, name):
        if name not in self.transactions[user.id]:
            return None
        else:
            return self.transactions[user.id][name]

    def create_row_in_transaction(self, user):
        ID = "".join((random.choice(string.ascii_lowercase) for _ in range(20)))

        # Row not created, just create it
        if not (ID in self.transactions[user.id].keys()):
            self.transactions[user.id][ID] = None

        # Returns the ID of the row
        return ID

class Test(TransactionalObject):
    def __init__(self, name: str, config) -> None:
        super().__init__()

        self.name = name
        self._logger = logging.getLogger(__name__)

        # Load systems
        self.systems = {}
        for cur_system in config["systems"]:
            delimiter = DEFAULT_CSV_DELIMITER
            if "delimiter" in cur_system:
                delimiter = cur_system["delimiter"]

            max_samples = -1
            if "max_samples" in cur_system:
                max_samples = cur_system["max_samples"]

            self.systems[cur_system["name"]] = (
                SystemManager().get(cur_system["data"].replace(".csv", ""), delimiter, max_samples),
            )


        # Create Test table in the database
        # NOTE: commit is delayed in order to enable to set later the foreign key constraint on needed columns
        self.model = ModelFactory().create(
            self.name, TestModel, commit=False
        )

        # Set the foreign key constraints
        foreign_key_for_each_system = []
        for system_name in self.systems.keys():
            foreign_key_for_each_system.append(
                (
                    system_name,
                    self.model.addColumn(
                        system_name,
                        db.Integer,
                        ForeignKey(SampleModel.__tablename__ + ".id"),
                    ),
                )
            )

        # Commit created table
        ModelFactory().commit(self.model)

        # Set relations between used samples and the current test
        for (system_name, foreign_key) in foreign_key_for_each_system:
            SampleModel.addRelationship(
                self.model.__name__ + "_" + system_name,
                self.model,
                uselist=True,
                foreign_keys=[foreign_key],
                backref="SampleModel_" + system_name,
            )

        # Set relations to associate multiple steps to a user
        StageModule.get_UserModel().addRelationship(
            self.model.__name__, self.model, uselist=True
        )

        # Initialize the sample selection strategy
        self._selection_strategy = FirstServerSelection(self.systems)


    def nb_steps_complete_by(self, user: UserModel) -> int:
        return len(getattr(user, self.model.__name__))


    def get_step(self, id_step: int, user: UserModel, nb_systems: int, is_intro_step:bool=False):
        """Get the samples needed for one step of the test
        """

        choice_for_systems = {}

        if self.has_transaction(user):
            return self.get_in_transaction(user, "choice_for_systems")
        else:
            # Select the systems
            self._logger.debug(f"Select systems for user {user.id}")
            pool_systems = self._selection_strategy.select_systems(nb_systems)

            # Select the samples
            self._logger.debug(f"Select samples for user {user.id}")
            for system_name in pool_systems:
                samples = self._selection_strategy.select_samples(system_name, 1) # NOTE: 1 is hardcoded here
                choice_for_systems[system_name] = samples[0]

            self._logger.info(f"This is what we will give to {user.id}: {choice_for_systems}")

            # Now we are ready to create the transaction
            self.create_transaction(user)

            # For each system, select the samples
            for system_name in choice_for_systems.keys():
                syssample = choice_for_systems[system_name]
                id_in_transaction = self.create_row_in_transaction(user)
                self.set_in_transaction(
                    user, id_in_transaction, (system_name, syssample.id)
                )
                choice_for_systems[system_name] = SampleModelTemplate(
                    id_in_transaction, system_name, syssample
                )

            # Define if it is an introduction step
            self.set_in_transaction(user, "intro_step", is_intro_step)

            # Set the systems/samples information
            self.set_in_transaction(user, "choice_for_systems", choice_for_systems)

            # Validate everything
            return choice_for_systems
