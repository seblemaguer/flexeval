# Import Libraries
import random
from datetime import datetime, timedelta

from flask import abort

from core.utils import get_provider, config, db
from core.mods.test.model.Sample import Sample
from core.mods.test.model.SystemSample import SystemSample
from core.mods.test.src.System import System
import core.mods.test as m_test

class Test():

    TESTS = {}
    DATA_ALREADY_MODIFIED = False

    @classmethod
    def get(cls,name):
        if not(name in cls.TESTS.keys()):
            cls.TESTS[name] = Test(name)
        return cls.TESTS[name]

    def __init__(self,name):
        self.name = name
        self.sample_in_eval={}



        anchors = []
        if name not in m_test.tests_data or name not in config["stages"]:
            raise Exception("Test "+name+" doesn't exist. Fix test.json.")

        if "time_out_delta_minutes" in config["stages"][name]:
            self.time_out_delta_minutes = int(config["stages"][name]["time_out_delta_minutes"])
        else:
            self.time_out_delta_minutes = 30

        if not("system_all_aligned" in m_test.tests_data[self.name]):
            m_test.tests_data[self.name]["system_all_aligned"] = True

        for data_system in m_test.tests_data[self.name]["systems"]:
            system = System(data_system["data"])

            if "aligned_with" in data_system:

                if  m_test.tests_data[self.name]["system_all_aligned"]:
                    if(not(Test.DATA_ALREADY_MODIFIED)):
                        raise Exception("TEST "+str(self.name)+": test.json say that systems are all aligned but an alignement between two systems have been specified. \n After fixing the test.json, don't forget to delete the current db that have been corrupted, before runing again the server.")

                anchor =  data_system["aligned_with"]
                anchor_data_system = None
                for _anchor_data_system in m_test.tests_data[self.name]["systems"]:
                    if(_anchor_data_system["name"] == anchor):
                        anchor_data_system = _anchor_data_system

                if anchor_data_system is None:
                    raise Exception("Test "+anchor+" doesn't exist. Fix test.json.")

                anchor_sys = System(anchor_data_system["data"])

                if not(anchor in anchors):
                    anchors.append(anchor)

                if not(len(anchor_sys.systemsamples) == len(system.systemsamples)):
                        raise Exception("TEST "+str(self.name)+": test.json say that systems: "+data_system["name"]+" and  "+anchor+ " are aligned, but they don't have the same number of sample (line). \n After fixing the csv of these systems or/and the test.json, don't forget to delete the current db that have been corrupted, before runing again the server.")

        if m_test.tests_data[self.name]["system_all_aligned"]:
            for data_system in m_test.tests_data[self.name]["systems"][1:]:
                data_system["aligned_with"] = m_test.tests_data[self.name]["systems"][0]["name"]
            Test.DATA_ALREADY_MODIFIED = True

        if("turn_nb_step" in config["stages"][name]):
            self.turn_nb_step = config["stages"][name]["turn_nb_step"]
        else:
            self.turn_nb_step = None


        if("turn_next" in config["stages"][name]):
            self.turn_next = config["stages"][name]["turn_next"]
        else:
            self.turn_next = config["stages"][name]["next"]

        self.nb_answers_max = config["stages"][name]["nb_answers"]

    def unique_system_answer(self):
        completed = Sample.query.filter_by(name_test=self.name,user=get_provider("auth").get()).all()

        unique_system_answer = 0
        for w in completed:
            if w.name_system == completed[0].name_system and w.question == completed[0].question:
                unique_system_answer = unique_system_answer + 1

        return unique_system_answer

    def set_systemsamples_in_eval(self,systemsamples):
        user = get_provider("auth").get()

        syssample = {}
        for name_system in systemsamples:
            syssample[name_system] =  systemsamples[name_system].id

        self.sample_in_eval[user] = {"date":datetime.now(),"syssample":syssample}

    def systemsamples_in_eval_has_timeout(self,skey):
        if(self.sample_in_eval[skey]["date"] + timedelta(minutes=self.time_out_delta_minutes) < datetime.now()):
            return True
        else:
            return False

    def close_systemsamples_in_eval(self):
        has_timeout = True

        try:
            user = get_provider("auth").get()
            has_timeout = self.systemsamples_in_eval_has_timeout(user)
            del self.sample_in_eval[user]

        except Exception as e:
            abort(408)

        if has_timeout:
            abort(408)

    def active_systemsamples_in_eval(self):
        user = get_provider("auth").get()

        if user in self.sample_in_eval.keys():
            return self.sample_in_eval[user]["syssample"]
        else:
            return None

    def numbers_of_systemsample_in_current_eval(self,name_system,systemsample):
        count = 0
        for skey in self.sample_in_eval.keys():
            try:
                if(not(self.systemsamples_in_eval_has_timeout(skey))):
                    id_syssample = self.sample_in_eval[skey]["syssample"][name_system]
                    if(systemsample.id == id_syssample):
                        count = count + 1
            except Exception as e:
                pass
        return count

    def get_system_sample_per_system(self,name_system,selected_systemsample_per_system):

        data_system = None
        for _data_system in m_test.tests_data[self.name]["systems"]:
            if(_data_system["name"] == name_system):
                data_system = _data_system

        if not(name_system in selected_systemsample_per_system.keys()):

            if "aligned_with" in data_system:
                name_system_anchor = data_system["aligned_with"]
                anchor_sys_samples = self.get_system_sample_per_system(name_system_anchor,selected_systemsample_per_system)
                selected_systemsample_per_system[name_system] = System(data_system["data"]).get_line(anchor_sys_samples.line_id)

            else:
                system = System(data_system["data"])
                choose_systemsample = []
                samples_per_systemsample_min = None

                for systemsample in system.systemsamples:

                    if(Sample.query.filter_by(  user = get_provider("auth").get(),
                                                system_sample_id = systemsample.id,
                                                name_test = self.name,
                                                name_system = name_system).first() is None):

                        samples = Sample.query.filter_by(   system_sample_id = systemsample.id,
                                                            name_test = self.name,
                                                            name_system = name_system).all()

                        number_sample_related_syssample = len(samples) + self.numbers_of_systemsample_in_current_eval(name_system,systemsample)

                        if( samples_per_systemsample_min is None):
                            samples_per_systemsample_min = number_sample_related_syssample
                            choose_systemsample.append(systemsample)

                        elif( number_sample_related_syssample == samples_per_systemsample_min):
                            choose_systemsample.append(systemsample)

                        elif( number_sample_related_syssample < samples_per_systemsample_min ):
                            choose_systemsample = [systemsample]
                            samples_per_systemsample_min = number_sample_related_syssample

                selected_systemsample_per_system[name_system] = random.choice(choose_systemsample)

        assert not(selected_systemsample_per_system[name_system] is None)

        return selected_systemsample_per_system[name_system]

    def get_system_sample(self):

        act = self.active_systemsamples_in_eval()
        selected_systemsample_per_system = {}

        if act is None:
            for data_system in m_test.tests_data[self.name]["systems"]:

                self.get_system_sample_per_system(data_system["name"],selected_systemsample_per_system)
        else:
            for act_key in act:
                selected_systemsample_per_system[act_key] = SystemSample.query.filter_by(id=act[act_key]).first()

        self.set_systemsamples_in_eval(selected_systemsample_per_system)
        return selected_systemsample_per_system
