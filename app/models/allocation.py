from ferris import BasicModel, ndb
from datetime import datetime, timedelta
from app.models.project import Project

class Allocation(BasicModel):
    project_id = ndb.KeyProperty()
    project_name = ndb.StringProperty() #temporarily store project_name
    color = ndb.StringProperty() #temporarily store color
    resource_name = ndb.StringProperty()
    alloc_hours = ndb.IntegerProperty()
    alloc_date = ndb.DateProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.project_id).fetch()
    
    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
