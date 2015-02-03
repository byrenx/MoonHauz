from ferris import BasicModel, ndb
from datetime import datetime, timedelta


class Allocation(BasicModel):
    project_id = ndb.KeyProperty()
    person_id = ndb.KeyProperty()
    start_date = ndb.DateTimeProperty()
    alloc_hours = ndb.IntegerProperty()
    end_date = ndb.DateTimeProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.project_id)
    
    @classmethod
    def create(cls, params):
        item = cls(project_id = params['project_id'],
                   person_id = params['person_id'],
                   start_date = params['start_date'],
                   alloc_hours = params['hours'],
                   end_date = params['start_date'] + timedelta(hours=params['hours'])
               )
        item.put()
        return item
    
    
