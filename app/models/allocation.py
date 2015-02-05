from ferris import BasicModel, ndb
from datetime import datetime, timedelta


class Allocation(BasicModel):
    project_id = ndb.KeyProperty()
    resource_name = ndb.StringProperty()
    alloc_hours = ndb.IntegerProperty()
    

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.project_id)
    
    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
