# Import Libraries
import random

from core.utils import get_provider, config, db
from core.mods.tests.model.Sample import Sample
from core.mods.tests.src.System import System
import core.mods.tests as m_test

class Test():

    TESTS = {}

    @classmethod
    def get(cld,name):
        if not(name in cls.TESTS.keys()):
            cls.TESTS[name] = Test(name)
        return cls.TESTS[name]

    def __init__(self,name):
        self.name = name

        if "system_aligned" in m_test.tests_data[name]:
            self.system_aligned = m_test.tests_data[name]["system_aligned"]
        else:
            self.system_aligned = True

        size_test = None
        for system in m_test.tests_data[self.name]["systems"]:
            system = System(system["data"])

            if self.system_aligned:
                if size_test is None:
                    size_test = len(system.systemsamples)
                else:
                    if not(size_test == len(system.systemsamples)):
                        raise Exception("TEST "+str(self.name)+": data.json say that the systems are aligned, but they don't have the same number of sample (line). \n After fixing the csv of these systems or/and the data.json, don't forget to delete the current db that have been corrupted, before runing again the server.")

        self.nb_answers_max = config["stages"][name]["nb_answers"]

    def unique_system_answer(self):
        completed = Sample.query.filter_by(name_test=self.name,user=get_provider("auth").get()).all()

        unique_system_answer = 0
        for w in completed:
            if w.name_system == completed[0].name_system and w.question == completed[0].question:
                unique_system_answer = unique_system_answer + 1

        return unique_system_answer

    def get_system_sample(self):

        selected_systemsample_per_system = {}

        for system in m_test.tests_data[self.name]["systems"]:
            name_system = system["name"]
            system = System(system["data"])

            if self.system_aligned and len(list(selected_systemsample_per_system.keys())) >= 1:
                selected_systemsample = selected_systemsample_per_system[list(selected_systemsample_per_system.keys())[0]]
                selected_systemsample_per_system[name_system] = system.get_line(selected_systemsample.line_id)

                assert not(selected_systemsample_per_system[name_system] is None)
            else:

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

        return selected_systemsample_per_system
