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
import hashlib
import shutil
from collections import OrderedDict

# Flask
from flask import current_app

# Flexeval
from flexeval.utils import AppSingleton
from flexeval.core import StageModule, UserModel
from flexeval.database import ForeignKey, ModelFactory, db
from flexeval.mods.test.model import TestModel, SampleModel

# Current package
from .System import SystemManager
from .selection_strategy import *

TEST_CONFIGURATION_BASENAME = "tests"
DEFAULT_CSV_DELIMITER = ","



class SampleModelTemplate:
    def __init__(self, id, system_name, systemsample):
        self._system = SystemManager().get(systemsample.system)
        self._systemsample = systemsample
        self.system_name = system_name
        self._ID = id
        self._cache = dict()
        self._cached = True # TODO: add as a configuration parameter

        if self._cached:
            self.CACHE_DIR=Path(current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/assets/tmp_eval")
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

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

            cur_sample_path = Path(current_app.config["FLEXEVAL_INSTANCE_DIR"] + "/systems" + file_path)
            try:
                if cur_sample_path.is_file():
                    if self._cached:
                        if cur_sample_path not in self._cache:
                            mime, _ = mimetypes.guess_type(cur_sample_path)
                            mime = mime.split("/")[0]
                            
                            extension = cur_sample_path.suffix

                            hashing = hashlib.md5()
                            hashing.update(str(cur_sample_path).encode())
                            value = self.CACHE_DIR/(str(hashing.hexdigest()) + extension)
                            shutil.copy(cur_sample_path, value)

                            value = str(value.relative_to(current_app.config["FLEXEVAL_INSTANCE_DIR"]))
                            # value = current_app.config["FLEXEVAL_INSTANCE_URL"] + "/" + str(value)
                            self._cache[cur_sample_path] = (value, mime)

                        return self._cache[cur_sample_path]
                else:
                    mime, _ = mimetypes.guess_type(cur_sample_path)
            except Exception as e:
                self._logger.warning("Exception was raised while reading sample attribute %s" % name)
                self._logger.warning(e)


                # with open(cur_sample_path, "rb") as f:
                #     data64 = base64.b64encode(f.read()).decode("utf-8")
                #     value = "data:%s;base64,%s" % (mime, data64)

                # mime = mime.split("/")[0]
            return (value, mime)

    def __str__(self):

        # return f"(Sys={self.system_name}, Sample={self._systemsample.audio})"
        return f"(Sys={self.system_name}, Sample={self._systemsample.__dict__})"
        # self._system = SystemManager().get(systemsample.system)
        # self._systemsample = systemsample
        # self.system_name = system_name
        # self._ID = id
        # self._cache = dict()
        # self._cached = True # TODO: add as a configuration parameter
        # pass

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
    
    def get_or_create_transaction(self, user):
        if not self.has_transaction(user):
            self.create_transaction(user)
        return self.get_transaction(user)

    def set_in_transaction(self, user, name, obj):
        self.transactions[user.id][name] = obj

    def get_in_transaction(self, user, name):
        if name not in self.transactions[user.id]:
            return None
        else:
            return self.transactions[user.id][name]
        
        
    def create_new_record(self, user, name=None):
        """Prepare a new record in the database (new line in the database after the user submits the form)

        Args:
            user: User to associate with the record
            name: Name for this record (useful when creating a field for a specific record). This ID will not be saved in the database.
        """
        # Dictionary "record name" -> list of field names
        user_transaction = self.get_or_create_transaction(user)
        all_records = user_transaction.setdefault("records", OrderedDict())
        if name == None:
            name = "record"+str(abs(hash("record"+str(len(all_records))))%int(1e9))
        name = name.replace(":","_") # Escape ":" as this is reserved for parsing identifiers
        current_fields = all_records.setdefault(name, list())
        return name

    def add_field_to_record(self, user, field_name, record_name=None):
        """Add a field to a current record

        Args:
            user: User to associate with the record
            field_name: Name of the field to add. If already existing, this is not added (duplicates are forbidden).
            record_name: Name of the record that will include the new field. If not defined, the field will be in the last record created. If no record does not exist, it is created.
        """
        user_transaction = self.get_or_create_transaction(user)
        all_records = user_transaction.setdefault("records", dict())
        # Create a record if no one exists yet
        if len(all_records) == 0:
            record_name = self.create_new_record(user, name=record_name)
        # Get the last record if at least one record exists and no record name has been given
        elif record_name == None:
            record_name = next(reversed(all_records))
        record_name = record_name.replace(":","_") # Escape ":" as this is reserved for parsing identifiers
        current_fields = self.get_fields_for_record(user, record_name)
        if field_name not in current_fields:
            current_fields.append(field_name)
            
        return record_name
            
    def get_all_records(self, user):
        user_transaction = self.get_or_create_transaction(user)
        all_records = user_transaction.setdefault("records", OrderedDict())
        return all_records
    
    def get_record(self, user, name=None):
        """Return the name of a record that exists

        Args:
            user: User to associate with the record
            name: Name for the target record. If it does not exists, it is created. If name is None, the last record is returned if any exists, a new record with an invinted name otherwise.
        """
        all_records = self.get_all_records(user)
        
        if name in all_records:
            return name
        else:
            if len(all_records) == 0 and name == None:
                return self.create_new_record(user)
            elif len(all_records) == 0 and name != None:
                return self.create_new_record(user, name=name)
            elif len(all_records) > 0 and name == None:
                return next(reversed(all_records))
            # elif len(all_records) > 0 and name != None:
            # Reminder: we already made sure that name is not present is all_records
            else:
                return self.create_new_record(user, name=name)
            
    def get_fields_for_record(self, user, record_name):
        """Return all fields associated to a given record

        Args:
            user: User for this record
            record_name: Name of the record. The record is created if not existing and empty list is returned (ie, no field associated).
        """
        user_transaction = self.get_or_create_transaction(user)
        all_records = user_transaction.setdefault("records", OrderedDict())
        current_fields = all_records.setdefault(record_name, list())
        return current_fields
        

    def create_row_in_transaction(self, user):
        ID = "".join((random.choice(string.ascii_lowercase) for _ in range(20)))

        # Row not created, just create it
        if not (ID in self.transactions[user.id].keys()):
            self.transactions[user.id][ID] = None

        # Returns the ID of the row
        return ID


class Test(TransactionalObject):
    def __init__(self, name: str, config) -> None:
        """Constructor

        Parameters
        ----------
        name: str
            The name of the section
        config: ????
            The configuration of the test

        """
        super().__init__()

        self.name = name
        self._logger = logging.getLogger(f"{__name__} ({self.name})")

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
        if "selection_strategy" in config:
            selection_strategy_name = config["selection_strategy"]
            self._logger.info(f"The selection strategy is user defined to \"{selection_strategy_name}\"")
            constructor = globals()[selection_strategy_name]
            self._selection_strategy = constructor(self.systems)
        else:
            self._logger.info(f"The selection strategy is defaulted to \"LeastSeenSelection\"")
            self._selection_strategy = LeastSeenSelection(self.systems)


    def nb_steps_complete_by(self, user: UserModel) -> int:
        """Get the number of steps completed by a given user

        Parameters
        ----------
        user: UserModel
           The scrutinized user

        Returns
        -------
        int
            The number of steps completed by the user
        """
        return len(getattr(user, self.model.__name__))


    def get_step(self, id_step: int, user: UserModel, nb_systems: int, is_intro_step:bool=False) -> Dict[str, SampleModelTemplate]:
        """Get the samples needed for one step of the test

        Parameters
        ----------
        id_step: int
            The index of the step
        user: UserModel
            The model of the participant to the step
        nb_systems: int
            The number of system wanted for the current step
        is_intro_step: bool
            Flag to indicate if the current step is an introduction step or not

        Returns
        -------
        Dict[str, SampleModelTemplate]
            The dictionnary associating which each system (name) the sample used
        """

        choice_for_systems = dict()
        if self.has_transaction(user):
            return self.get_in_transaction(user, "choice_for_systems")
        else:

            # Select samples (NOTE: 1 is hardcoded here)
            selected_samples = self._selection_strategy.select_samples(user.id, nb_systems, 1) #
            for system_name, samples in selected_samples.items():
                choice_for_systems[system_name] = samples[0]

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
