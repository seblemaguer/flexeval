# coding: utf8
from .extensions import db
from .utils import AppSingleton
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect

# From cookie cutter
# https://github.com/cookiecutter-flask/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/database.py

# Alias common SQLAlchemy names
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship

# Helper's function
def commit_all():
    db.session.commit()

class DataBaseError(Exception):

    def __init__(self,message):
        self.message = message

class ConstraintsError(DataBaseError):
    pass

class MalformationError(DataBaseError):
    pass

class ForbiddenColumnName(DataBaseError):
    pass

class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create a new record and save it the database."""

        for name_col in kwargs.keys():
            if name_col == "commit":
             raise ForbiddenColumnName("Col name: commit is forbidden.")

        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self,*args,**kwargs)

    @classmethod
    def addRelationship(cls,name,TargetClass,**kwargs):

        if not(hasattr(cls,name)):
            setattr(cls,name,relationship(TargetClass.__name__,**kwargs))

    @classmethod
    def addColumn(cls,name,col_type,*constraints):

        if not(hasattr(cls,name)):
            column = Column(col_type,*constraints)
            setattr(cls,name,column)

            if not(name.replace("_","").isalnum()):
                raise MalformationError("Col name:"+name+" is incorrect. Only alphanumeric's and '_' symbol caracteres are allow. ")

            if db.engine.dialect.has_table(db.engine,cls.__tablename__):

                name_columns_in_table = [col_in_table["name"] for col_in_table in inspect(db.engine).get_columns(cls.__tablename__)]
                if name not in name_columns_in_table:

                    column_type = column.type.compile(db.engine.dialect)
                    db.engine.execute("ALTER TABLE '%s' ADD COLUMN %s %s" % (cls.__tablename__, name, column_type))

                    if len(constraints) > 0:
                        raise ConstraintsError("Table "+cls.__tablename__+" already existing. Due to SQLite limitation, you can't add a constraint via ALTER TABLE ___ ADD COLUMN ___ .")
            return column
        else:
            return getattr(cls,name)

class ModelFactory(metaclass=AppSingleton):

    def __init__(self):
        self.register={}

    def get(self,name_table,base):
        try:
            return self.register[base.__name__+"_"+name_table]
        except Exception as e:
            return None

    def create(self,name_table, base, commit=True):
        if not(base.__name__+"_"+name_table in self.register):
            if(Model in base.__bases__):
                assert base.__abstract__

            if db.engine.dialect.has_table(db.engine, base.__name__+"_"+name_table):
                self.register[base.__name__+"_"+name_table] = type(base.__name__+"_"+name_table, (base,Model,), {
                                                                            "__tablename__":base.__name__+"_"+name_table,
                                                                            "__table_args__":
                                                                            {
                                                                                'extend_existing': True,
                                                                                'autoload':True,
                                                                                'autoload_with': db.engine
                                                                            }
                                                                        })
            else:
                self.register[base.__name__+"_"+name_table] = type(base.__name__+"_"+name_table, (base,Model,), {
                                                                            "__tablename__":base.__name__+"_"+name_table,
                                                                            "__table_args__":
                                                                            {
                                                                                'extend_existing': True
                                                                        }
                                                                    })

        if commit:
            return self.commit(self.register[base.__name__+"_"+name_table])
        else:
            return self.register[base.__name__+"_"+name_table]


    def commit(self,cls):
        if not(db.engine.dialect.has_table(db.engine,cls.__tablename__)):
            cls.__table__.create(db.engine)

        return cls
