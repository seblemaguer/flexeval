# coding: utf8
import json
import random
import string
from pathlib import Path
import base64
import mimetypes
from datetime import datetime,timedelta

from flask import current_app

from flexeval.utils import AppSingleton
from flexeval.core import StageModule
from flexeval.database import Column,ForeignKey,ModelFactory,db

from flexeval.mods.test.model import TestSample, SystemSample

from .System import SystemManager

class SystemSampleTemplate():

    def __init__(self,id,system_name,systemsample):
        self._system = SystemManager().get(systemsample.system)
        self._systemsample = systemsample
        self.system_name = system_name
        self._ID = id

    @property
    def ID(self):
        return self._ID

    def get(self,name=None,num=None):
        if num is not None:
            name = self._system.cols_name[num]

        if name is None:
            return (None,None)
        else:

            mime = "text"
            value = getattr(self._systemsample,name)

            file_path = value

            if not(file_path[0] == "/"):
                file_path = "/"+file_path

            if(Path(current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/systems"+file_path).is_file()):
                mime, _ = mimetypes.guess_type(current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/systems"+file_path)

                with open(current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/systems"+file_path, 'rb') as f:
                    data64 = base64.b64encode(f.read()).decode('utf-8')
                    value = u'data:%s;base64,%s' % (mime, data64)
                mime = mime.split("/")[0]

            return (value,mime)

class TestError(Exception):

    def __init__(self,message):
        self.message = message

class MalformationError(TestError):
    pass

class TestManager(metaclass=AppSingleton):

    def __init__(self):
        self.register={}

        with open(current_app.config["FLEXEVAL_INSTANCE_DIR"]+'/tests.json',encoding='utf-8') as config:
            self.config = json.load(config)

    def get(self,name):
        if not(name in self.register):
            try:
                config = self.config[name]
            except Exception as e:
                raise MalformationError("Test "+name+" not found in tests.json .")
            self.register[name] = Test(name,config)

        return self.register[name]

class Test():

    def __init__(self,name,config):

        # Init l'objet Test
        self.name = name
        self.systems = {}
        self.transactions = {}
        self.time_out_seconds = 3600

        if "system_all_aligned" in config:
            system_all_aligned = config["system_all_aligned"]
        else:
            system_all_aligned = True

        try:
            assert isinstance(system_all_aligned,bool)
        except Exception as e:
            raise MalformationError("system_all_aligned need to be a boolean value.")

        for system_i,system in enumerate(config["systems"]):

            aligned_with=None

            if "aligned_with" in system:
                if config["system_all_aligned"]:
                    raise MalformationError("You can't specified a field 'aligned_with' if the system are all aligned (default behavior). ")
                else:
                    aligned_with = system["aligned_with"]

            if system_all_aligned and system_i > 0:
                aligned_with = config["systems"][0]["name"]

            self.systems[system["name"]] = (SystemManager().get(system["data"].replace(".csv","")),aligned_with)

        # Init ou Regen la repr en bdd & les relations

        # TestSample établie une relation TestSample -> User
        # On ne commit pas cad on ne crée pas la table en BDD directement après create (commit=False)
        # Si la table est créée on ne peut pas ajouter de contrainte (ForeignKey) à une colonne.
        self.testSampleModel = ModelFactory().create(self.name,TestSample,commit=False)

        foreign_key_for_each_system=[]
        for system_name in self.systems.keys():
            foreign_key_for_each_system.append((system_name,self.testSampleModel.addColumn(system_name,db.Integer,ForeignKey(SystemSample.__tablename__+".id"))))

        # Une fois les clefs étrang. gen on créée la table
        ModelFactory().commit(self.testSampleModel)

        # On utilise les clefs etrang. nouvellement créées pour gen les relations bidirect. entre self.testSampleModel <-> SystemSample
        for (system_name,foreign_key) in foreign_key_for_each_system:
            #self.testSampleModel.addRelationship("SystemSample_"+system_name,SystemSample,uselist=False,foreign_keys=[foreign_key])
            SystemSample.addRelationship(self.testSampleModel.__name__+"_"+system_name,self.testSampleModel,uselist=True,foreign_keys=[foreign_key], backref="SystemSample_"+system_name)

        # On établie la relation One User -> Many TestSample
        StageModule.get_UserModel().addRelationship(self.testSampleModel.__name__,self.testSampleModel,uselist=True)

    def set_timeout_for_transaction(self,timeout):
        self.time_out_seconds = timeout

    def delete_transaction(self,user):
        del self.transactions[user.pseudo]

    def create_transaction(self,user):
        self.transactions[user.pseudo] = {"date":datetime.now()}

    def get_transactions(self):

        transactions = []
        to_del = []

        for key_transaction in self.transactions.keys():
            transaction = self.transactions[key_transaction]

            if (self.time_out_seconds is not None) and (transaction["date"] + timedelta(seconds=self.time_out_seconds) < datetime.now()):
                to_del.append(key_transaction)
            else:
                transactions.append(transaction)

        for transaction_key_to_del in to_del:
            del self.transactions[transaction_key_to_del]

        return transactions

    def has_transaction(self,user):
        return user.pseudo in self.transactions

    def get_transaction(self,user):
        return self.transactions[user.pseudo]

    def set_in_transaction(self,user,name,obj):
        self.transactions[user.pseudo][name] = obj

    def get_in_transaction(self,user,name):
        if name not in self.transactions[user.pseudo]:
            return None
        else:
            return self.transactions[user.pseudo][name]

    def create_row_in_transaction(self,user):
        ID = ''.join((random.choice(string.ascii_lowercase) for i in range(20)))
        if ID in self.transactions[user.pseudo].keys():
            return self.create_row_in_transaction()
        else:
            self.transactions[user.pseudo][ID] = None
            return ID

    def nb_steps_complete_by(self,user):
        return len(getattr(user,self.testSampleModel.__name__))

    def choose_syssample_for_system(self,user,system_name):
        (system,aligned_with) = self.systems[system_name]

        assert aligned_with is None

        choices = []
        min_times_syssample_have_been_selected = None

        system_syssamples = system.system_samples

        transactions = self.get_transactions()
        syssample_in_process = {}
        for transaction in transactions:

            if "choice_for_systems" in transaction:

                intro_step = transaction["intro_step"]

                if not(intro_step):
                    if "choice_for_systems" in transaction:
                        idsyssample = transaction["choice_for_systems"][system_name]._systemsample.id

                        if idsyssample in syssample_in_process:
                            syssample_in_process[str(idsyssample)] = syssample_in_process[str(idsyssample)] + 1
                        else:
                            syssample_in_process[str(idsyssample)] =  1

        for syssample in system_syssamples:

            syssample_already_seen_by_user = []
            for tSample in getattr(user,self.testSampleModel.__name__):
                if not(tSample.intro): # Si le testSample correspond à un testSample d'intro, on ne le compte pas pour le brassage.
                    syssample_already_seen_by_user.append(getattr(tSample,"SystemSample_"+system_name))

            if not(syssample in syssample_already_seen_by_user):

                nb_times_syssample_have_been_selected = len(getattr(syssample,self.testSampleModel.__name__+"_"+system_name))
                if str(syssample.id) in syssample_in_process:
                    nb_times_syssample_have_been_selected = syssample_in_process[str(syssample.id)] + nb_times_syssample_have_been_selected

                if(min_times_syssample_have_been_selected is None):
                    min_times_syssample_have_been_selected = nb_times_syssample_have_been_selected
                    choices.append(syssample)
                elif(min_times_syssample_have_been_selected == nb_times_syssample_have_been_selected):
                    choices.append(syssample)
                elif(min_times_syssample_have_been_selected > nb_times_syssample_have_been_selected):
                    min_times_syssample_have_been_selected = nb_times_syssample_have_been_selected
                    choices = [syssample]

        if len(choices) == 0:
            choices = system.system_samples

        return random.choice(choices)

    def make_same_choice_syssample(self,system_name,syssample_source):
        (system,aligned_with) = self.systems[system_name]
        return system.system_samples[syssample_source.line_id]

    def get_syssample_for_step(self,choice_for_systems,system_name,user):
        (system,aligned_with) = self.systems[system_name]

        if system_name in choice_for_systems:
            choice_for_systems[system_name]
        else:
            if aligned_with is None:
                choice_for_systems[system_name] = self.choose_syssample_for_system(user,system_name)
            else:
                if not(aligned_with in choice_for_systems):
                    self.get_syssample_for_step(choice_for_systems,aligned_with,user)

                choice_for_systems[system_name] = self.make_same_choice_syssample(system_name,choice_for_systems[aligned_with])

    def get_step(self,user,is_intro_step=False):

        choice_for_systems={}

        if self.has_transaction(user):
            return self.get_in_transaction(user,"choice_for_systems")
        else:

            self.create_transaction(user)

            for system_name in self.systems.keys():
                self.get_syssample_for_step(choice_for_systems,system_name,user)

            for system_name in choice_for_systems.keys():
                (system,aligned_with) = self.systems[system_name]
                syssample = choice_for_systems[system_name]

                id_in_transaction = self.create_row_in_transaction(user)
                self.set_in_transaction(user,id_in_transaction,(system_name,syssample.id))
                choice_for_systems[system_name] = SystemSampleTemplate(id_in_transaction,system_name,syssample)

            self.set_in_transaction(user,"intro_step",is_intro_step)
            self.set_in_transaction(user,"choice_for_systems",choice_for_systems)

            return choice_for_systems
