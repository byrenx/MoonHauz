#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class CondoUnit(Property):
    capacity = ndb.IntegerProperty(required=False)
    bedrooms = ndb.IntegerProperty(required=False)
    floor_area = ndb.FloatProperty(required=False)

    @classmethod
    def list_all(cls):
        return cls.query()
