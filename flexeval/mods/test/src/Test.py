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
from flexeval.core import StageModule, UserBase
from flexeval.database import ForeignKey, ModelFactory, db
from flexeval.mods.test.model import TestModel, SystemSample

# Current package
from .System import SystemManager

TEST_CONFIGURATION_BASENAME = "tests"
DEFAULT_CSV_DELIMITER = ","


class SystemSampleTemplate:
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
        del self.transactions[user.pseudo]

    def create_transaction(self, user):
        self.transactions[user.pseudo] = {"date": datetime.now()}

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
        return user.pseudo in self.transactions

    def get_transaction(self, user):
        return self.transactions[user.pseudo]

    def set_in_transaction(self, user, name, obj):
        self.transactions[user.pseudo][name] = obj

    def get_in_transaction(self, user, name):
        if name not in self.transactions[user.pseudo]:
            return None
        else:
            return self.transactions[user.pseudo][name]

    def create_row_in_transaction(self, user):
        ID = "".join((random.choice(string.ascii_lowercase) for _ in range(20)))

        # Row not created, just create it
        if not (ID in self.transactions[user.pseudo].keys()):
            self.transactions[user.pseudo][ID] = None

        # Returns the ID of the row
        return ID

class Test(TransactionalObject):
    def __init__(self, name, config):
        super().__init__()

        # Init l'objet Test
        self.name = name
        self.systems = {}

        if "system_all_aligned" in config:
            system_all_aligned = config["system_all_aligned"]
        else:
            system_all_aligned = True

        try:
            assert isinstance(system_all_aligned, bool)
        except Exception as e:
            raise MalformationError("system_all_aligned need to be a boolean value.")

        for system_i, system in enumerate(config["systems"]):

            aligned_with = None

            if "aligned_with" in system:
                if config["system_all_aligned"]:
                    raise MalformationError(
                        "You can't specified a field 'aligned_with' if the system are all aligned (default behavior). "
                    )
                else:
                    aligned_with = system["aligned_with"]

            if system_all_aligned and system_i > 0:
                aligned_with = config["systems"][0]["name"]

            delimiter = DEFAULT_CSV_DELIMITER
            if "delimiter" in system:
                delimiter = system["delimiter"]

            self.systems[system["name"]] = (
                SystemManager().get(system["data"].replace(".csv", ""), delimiter),
                aligned_with,
            )

        # Init ou Regen la repr en bdd & les relations

        # TestModel établie une relation TestModel -> User
        # On ne commit pas cad on ne crée pas la table en BDD directement après create (commit=False)
        # Si la table est créée on ne peut pas ajouter de contrainte (ForeignKey) à une colonne.
        self.model = ModelFactory().create(
            self.name, TestModel, commit=False
        )

        foreign_key_for_each_system = []
        for system_name in self.systems.keys():
            foreign_key_for_each_system.append(
                (
                    system_name,
                    self.model.addColumn(
                        system_name,
                        db.Integer,
                        ForeignKey(SystemSample.__tablename__ + ".id"),
                    ),
                )
            )

        # Une fois les clefs étrang. gen on créée la table
        ModelFactory().commit(self.model)

        # On utilise les clefs etrang. nouvellement créées pour gen les relations bidirect. entre self.model <-> SystemSample
        for (system_name, foreign_key) in foreign_key_for_each_system:
            SystemSample.addRelationship(
                self.model.__name__ + "_" + system_name,
                self.model,
                uselist=True,
                foreign_keys=[foreign_key],
                backref="SystemSample_" + system_name,
            )

        # On établie la relation One User -> Many TestModel
        StageModule.get_UserModel().addRelationship(
            self.model.__name__, self.model, uselist=True
        )


    def nb_steps_complete_by(self, user: UserBase) -> int:
        return len(getattr(user, self.model.__name__))

    def select_systems(self, nb_systems: int) -> List[str]:

        # Get the total amount of time a system is seen
        system_counts = {}
        for system_name, system_info in self.systems.items():
            (system, _) = system_info
            system_counts[system_name] = 0

            # Count the samples number of samples
            for syssample in system.system_samples:
                system_counts[system_name] += len(getattr(syssample, self.model.__name__ + "_" + system_name))

        # Don't forget the one which are in transactions
        transactions = self.get_transactions()
        for transaction in transactions:
            if "choice_for_systems" in transaction:
                if ("choice_for_systems" in transaction) and \
                   ("system_name" in transaction["choice_for_systems"]):
                    system_name = transaction["choice_for_systems"]["system_name"]._systemsample.system
                    system_counts[system_name] += 1


        # Compute list
        count_systems = {}
        for system_name, count in system_counts.items():
            if count not in count_systems:
                count_systems[count] = [system_name]
            else:
                count_systems[count].append(system_name)
        self._logger.info(f"The systems sorted by occurrences is {count_systems}")

        # Randomize by prioritizing the system seen the minimum amount of time
        pool_systems = []
        sorted_counts = list(count_systems.keys())
        sorted_counts.sort();
        remaining = nb_systems
        for cur_count in sorted_counts:
            available_systems = count_systems[cur_count]
            if len(available_systems) >= remaining:
                pool_systems += random.choices(available_systems)
            else:
                pool_systems += random.choices(available_systems[:remaining])

            remaining -= len(count_systems[cur_count])

            if remaining <= 0:
                break

        # Return the number of needed systems
        return pool_systems


    def choose_syssample_for_system(self, user, system_name):
        (system, _) = self.systems[system_name]

        transactions = self.get_transactions()
        syssample_in_process = {}

        for transaction in transactions:
            if "choice_for_systems" in transaction:

                if ("choice_for_systems" in transaction) and \
                   ("system_name" in transaction["choice_for_systems"]):
                    idsyssample = transaction["choice_for_systems"][
                        system_name
                    ]._systemsample.id

                    if idsyssample in syssample_in_process:
                        syssample_in_process[str(idsyssample)] = (
                            syssample_in_process[str(idsyssample)] + 1
                        )
                    else:
                        syssample_in_process[str(idsyssample)] = 1


        # Ignore samples already seen by the users
        syssample_already_seen_by_user = set()
        for tSample in getattr(user, self.model.__name__):
            syssample_already_seen_by_user.add(
                getattr(tSample, "SystemSample_" + system_name)
            )
        available_samples = set(system.system_samples).difference(syssample_already_seen_by_user)

        # List samples for system by ascending counts
        count_samples = dict()
        for sample in available_samples:
            sample_selected_count = len(
                getattr(
                    sample, self.model.__name__ + "_" + system_name
                )
            )
            if sample_selected_count not in count_samples:
                count_samples[sample_selected_count] = []
            count_samples[sample_selected_count].append(sample)


        # Select the sample with the priority of the less seen sample
        sorted_counts = list(count_samples.keys())
        sorted_counts.sort();

        rand_sample = random.choice(count_samples[sorted_counts[0]])
        return rand_sample

    def get_syssample_for_step(self, choice_for_systems, system_name, user):
        choice_for_systems[system_name] = self.choose_syssample_for_system(
            user, system_name
        )

    def get_step(self, user, nb_systems, is_intro_step=False):

        choice_for_systems = {}

        if self.has_transaction(user):
            return self.get_in_transaction(user, "choice_for_systems")
        else:

            self.create_transaction(user)

            # Select the systems
            pool_systems = self.select_systems(nb_systems)
            for system_name in pool_systems:
                self.get_syssample_for_step(choice_for_systems, system_name, user)

            # For each system, select the samples
            for system_name in choice_for_systems.keys():
                syssample = choice_for_systems[system_name]
                id_in_transaction = self.create_row_in_transaction(user)
                self.set_in_transaction(
                    user, id_in_transaction, (system_name, syssample.id)
                )
                choice_for_systems[system_name] = SystemSampleTemplate(
                    id_in_transaction, system_name, syssample
                )

            # Define if it is an introduction step
            self.set_in_transaction(user, "intro_step", is_intro_step)

            # Set the systems/samples information
            self.set_in_transaction(user, "choice_for_systems", choice_for_systems)

            # Validate everything
            return choice_for_systems
