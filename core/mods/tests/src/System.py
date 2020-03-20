# Import Libraries
import csv
import random
import string

from core.mods.tests.model.SystemSample import SystemSample
from core.utils import NAME_REP_CONFIG,db


class System():

    def __init__(self,source):
        self.source = source
        systemsamples = SystemSample.query.filter_by(source=self.source).all()

        if(len(systemsamples) == 0):

            reader = csv.DictReader(open(NAME_REP_CONFIG+"/systems/"+self.source))
            for line_id, line in enumerate(reader):
                line_value = []
                for line_key in list(line.keys()):
                    line_value.append({line_key:line[line_key]})

                systemsample = SystemSample(line_id,line_value,self.source)
                db.session.add(systemsample)
                systemsamples.append(systemsample)

            db.session.commit()

        self.systemsamples = systemsamples

    def get_line(self,id):
        return SystemSample.query.filter_by(source=self.source,line_id=id).first()


class SystemTemplate():

    REMINDER = {}

    def __init__(self, name_system, systemsample):
        self.name_system = name_system
        self.data = {}
        self.column_name = []
        self.systemsample_id = systemsample.id

        for l in systemsample.line_value:
            k = list(l.keys())[0]
            self.data[k] = l[k]
            self.column_name.append(k)

    @classmethod
    def set_reminder(cls,json_data):
        key = ''.join((random.choice(string.ascii_lowercase) for i in range(256)))
        cls.REMINDER[key] = json_data

        return key

    @classmethod
    def get_reminder(cls,key):
        json_data = SystemTemplate.REMINDER[key]
        del cls.REMINDER[key]

        return json_data

    def name(self):
        key = SystemTemplate.set_reminder({"name_system": self.name_system})
        return "@SystemTemplate:"+str(key)

    @classmethod
    def get_name(cls,val):
        base = "@SystemTemplate:"
        split = val.split("@SystemTemplate:")

        if(len(split) == 2):
            return SystemTemplate.get_reminder(split[1])["name_system"]
        else:
            return None

    @classmethod
    def get_save_field(cls,field):
        base = "@SystemTemplate:"
        split = field.split("@SystemTemplate:")

        if(len(split) == 2):
            return (split[0],SystemTemplate.get_reminder(split[1]))
        else:
            return None

    @classmethod
    def save_field(cls,name_field,systems):

        if not(isinstance(systems,list)):
            systems=[systems]

        systems_reminder = []

        for system in systems:
            systems_reminder.append({"systemsample_id":system.systemsample_id,"name_system":system.name_system})

        key = SystemTemplate.set_reminder(systems_reminder)

        return name_field+"@SystemTemplate:"+str(key)

    def get_column_name(self,i):
        return self.column_name[i]
