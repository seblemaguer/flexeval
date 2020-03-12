from sqlalchemy import orm
from utils import db, config, NAME_REP_CONFIG
import csv
from mods.tests.model.Sample import Sample

class SystemSample(db.Model):
    __tablename__ = 'systemsample'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    value = db.Column(db.String,nullable=False)
    sample_id = db.Column(db.Integer,nullable=False)
    system = db.Column(db.String,nullable=False)

    def __init__(self,name,value,sample_id,system):

        self.name = str(name)
        self.value = str(value)
        self.sample_id = sample_id
        self.system = system


class SysSample():

    id = 0
    
    def __init__(self,components,system,id=None):
        self._components = None
        self.components = []
        self._samples=[]


        if id is None:
            for key in components.keys():
                ssample = SystemSample(key,components[key],SysSample.id,system)
                self.add(ssample)
                db.session.add(ssample)
            SysSample.id = SysSample.id + 1
            db.session.commit()
        else:
            self.id = id
            for s in  Sample.query.filter_by(syssample_id=self.id).all():
                self._samples.append(s.id)

    def add(self,component):
        self.components.append(component)

    @property
    def json(self):
        if self._components is None:
            self._components = {}

            for component in self.components:
                self._components[component.name] = component.value

        return self._components

    def samples(self):
        rtn = []
        for id in self._samples:
            rtn.append(Sample.query.filter_by(id=id).first())

        return rtn

    def add_sample(self,question,answer,name,user_id):

        sample = Sample(question,answer,name,user_id)
        sample.syssample_id = self.id
        db.session.add(sample)
        db.session.commit()
        self._samples.append(sample.id)

    def save_field(self,name_field):
        return name_field+"_SysSample_"+str(self.id)

    @classmethod
    def get_save_field(self,field):
        split = field.split("_SysSample_")

        if(len(split) == 2):
            return split
        else:
            return None

class System():

    SYSTEMS = {}

    @classmethod
    def get(cls,name):
        if name in System.SYSTEMS.keys():
            return System.SYSTEMS[name]
        else:
            sys = System(name)
            System.SYSTEMS[name] = sys
            return sys

    def __init__(self,system):

        self._samples = {}
        self.system = None

        source = NAME_REP_CONFIG+'/systems/'+ system
        try:
            sysamples = SystemSample.query.filter_by(system=system).all()
            assert not(len(sysamples) == 0)

            for sysample in sysamples:
                if(not(sysample.sample_id in self._samples.keys())):
                    ssample = SysSample(None,None,sysample.sample_id)
                    self._samples[sysample.sample_id] = ssample
                else:
                    ssample = self._samples[sysample.sample_id]

                ssample.add(sysample)

        except Exception as e:
            reader = csv.DictReader(open(source))
            for r in reader:
                ssample = SysSample(r,system)
                self._samples[ssample.id] = ssample
        self.system = system

    @classmethod
    def get_syssample(cls,id):
        id = int(id)
        for sys in System.SYSTEMS.keys():
            sys =  System.SYSTEMS[sys]

            if id in sys._samples.keys():
                return sys._samples[id]

    @property
    def samples(self):
        return list(self._samples.values())
