from ferris import BasicModel, ndb
from datetime import timedelta
import datetime


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
        print params['start_date']
        item = cls(name = params['name'],
                   billable_hours = params['billable_hours'],
                   start_date = datetime.datetime.utcfromtimestamp(float(params['start_date']))
               )
        item.put()
        return item
