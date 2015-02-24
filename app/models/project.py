from ferris import BasicModel, ndb
from datetime import timedelta
import datetime


class Project(BasicModel):
    name = ndb.StringProperty()
    billable_hours = ndb.IntegerProperty()
    start_date = ndb.DateTimeProperty()
    remaining_hours = ndb.IntegerProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.name)

    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query(cls.key == project_id).fetch()[0]

    @classmethod
    def find_by_proj_key(cls, project_id):
        return cls.query(cls.key == project_id).fetch()

    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def update(self, params):
        self.populate(**params)
        self.put()

    @classmethod
    def updateHours(self, params,key):
        data = self.query(self.key == key).fetch()
        print repr(data)
        data[0].remaining_hours=params['remaining_hours']
        data[0].put()

    @classmethod
    def retHours(self, params, hours):
        params[0].remaining_hours+=hours
        print params[0].remaining_hours
        params[0].put()

    @classmethod
    def removeHours(self, params, hours):
        params[0].remaining_hours-=hours

        params[0].put()

        return params[0].remaining_hours

    @classmethod
    def create(cls, params):
        item = cls(name = params['name'],
                   billable_hours = params['billable_hours'],
                   remaining_hours = params['billable_hours'],
                   start_date = datetime.datetime.utcfromtimestamp(float(params['start_date']))
               )
        item.put()
        return item
