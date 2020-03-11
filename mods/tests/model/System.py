from sqlalchemy import orm
from utils import db, config
import csv
from mods.tests.model.Sample import Sample
G_systems = {}

class SysSampleComponent(db.Model):
    __tablename__ = 'syssamplecomponent'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    value = db.Column(db.String,nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('syssample.id'))

    def __init__(self,name,value):

        self.name = str(name)
        self.value = str(value)


class SysSample(db.Model):
    __tablename__ = 'syssample'

    id = db.Column(db.Integer, primary_key=True)
    component = db.relationship('SysSampleComponent')
    samples = db.relationship('Sample')
    source = db.Column(db.String,nullable=False)
    _components = None

    def __init__(self,components,source):

        self.source = source
        for key in components.keys():
            self.component.append(SysSampleComponent(key,components[key]))

    @property
    def json(self):
        if self._components is None:
            self._components = {}

            for component in self.component:
                self._components[component.name] = component.value

        return self._components

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


    _samples = None
    source = None

    @classmethod
    def get(cls,source):
        if source in G_systems.keys():
            return G_systems[source]
        else:
            return System(source)

    def __init__(self,source):

        try:
            OneSample = SysSample.query.filter_by(source=source).first()
            assert not(OneSample is None)
        except Exception as e:
            reader = csv.DictReader(open(source))
            for r in reader:
                db.session.add(SysSample(r,source))
            db.session.commit()
        self.source = source

    def samples(self):
        if self._samples is None:
            self._samples = []

            for sample in SysSample.query.filter_by(source=self.source).all():
                self._samples.append(sample)

        return self._samples
