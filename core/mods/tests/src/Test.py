# Import Libraries
import random

from core.utils import get_provider, config, db
from core.mods.tests.model.Sample import Sample
from core.mods.tests.src.System import System
import core.mods.tests as m_test

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

        anchors = []
        orphelins = []

        size_test = None
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

                        if( samples_per_systemsample_min is None):
                            samples_per_systemsample_min = len(samples)
                            choose_systemsample.append(systemsample)

                        elif( len(samples) == samples_per_systemsample_min):
                            choose_systemsample.append(systemsample)

                        elif( len(samples) < samples_per_systemsample_min ):
                            choose_systemsample = [systemsample]
                            samples_per_systemsample_min = len(samples)

                selected_systemsample_per_system[name_system] = random.choice(choose_systemsample)

        assert not(selected_systemsample_per_system[name_system] is None)
        return selected_systemsample_per_system[name_system]

    def get_system_sample(self):

        selected_systemsample_per_system = {}

        for data_system in m_test.tests_data[self.name]["systems"]:

            self.get_system_sample_per_system(data_system["name"],selected_systemsample_per_system)

        return selected_systemsample_per_system
