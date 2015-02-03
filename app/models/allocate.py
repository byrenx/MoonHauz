from ferris import BasicModel, ndb
from datetime import datetime, timedelta


class Allocate(BasicModel):
    project_id = ndb.KeyProperty()
    person_id = ndb.KeyProperty()
    start_date = ndb.DateTimeProperty()
    total_hours = ndb.IntegerProperty()
    end_date = ndb.DateTimeProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.start_date)
    
    @classmethod
    def create(cls, params):
        item = cls(project_id = params['project_id'],
                   person_id = params['person_id'],
                   start_date = params['start_date'],
                   total_hours = params['total_hours'],
                   end_date = params['start_date'] + timedelta(hours=params['total_hours'])
               )
        item.put()
        return item
    
