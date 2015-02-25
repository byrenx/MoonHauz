from ferris import BasicModel, ndb
from datetime import datetime, timedelta
from app.behaviors.eventbehavior import EventBehavior
from google.appengine.ext import deferred

class Event(BasicModel):
    allocation_id = ndb.KeyProperty()
    start_date = ndb.DateProperty()
    end_date = ndb.DateProperty()
    frequency = ndb.FloatProperty()
    total_hours = ndb.FloatProperty()

    class Meta:
        behaviors = (EventBehavior, )

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.allocation_id).fetch()

    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item

    @classmethod
    def find_by_allocation(cls, id):
        return cls.query().filter(cls.allocation_id == id).order(cls.end_date).fetch()

    def delete(self):
        ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only=True))

    @classmethod
    def delete_by_alloc_id(cls,id):
        allocs = cls.find_by_allocation(id)
        for a in allocs:
            deferred.defer(cls.del_events, a.key.urlsafe())

    @classmethod
    def del_events(cls, key):
        key = ndb.Key(urlsafe=key)
        key.delete()
