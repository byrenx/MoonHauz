from ferris import BasicModel, ndb
from datetime import datetime, timedelta

class Project(BasicModel):
    name = ndb.StringProperty()
    billable_hours = ndb.IntegerProperty()
    start_date = ndb.DateTimeProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.name)
    
    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query().filter(cls.key == project_id)
    
    @classmethod
    def update(self, params):
        self.populate(**params)
        self.put()

    @classmethod
    def create(cls, params):
        item = cls(name = params['project_id'],
                   billable_hours = params['billable_hours'],
                   start_date = params['start_date'],
                   end_date = params['start_date'] + timedelta(hours=params['billable_hours'])
               )
        item.put()
        return item
