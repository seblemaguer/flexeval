from mods.tests.model.SystemSample import SystemSample
from utils import NAME_REP_CONFIG,db
import csv

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
    def get_save_field(cls,field):
        split = field.split("_SystemSample_")

        if(len(split) == 2):
            return split
        else:
            return None

    def save_field(self,name_field):
        return name_field+"_SystemSample_"+str(self.systemsample_id)

    def get_column_name(self,i):
        return self.column_name[i]
