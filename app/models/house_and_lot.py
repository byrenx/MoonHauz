#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class HouseAndLot(Property):
    floors = ndb.IntegerProperty(required=True, default=1)
    bedrooms = ndb.IntegerProperty(required=True)
    floor_area = ndb.FloatProperty()
    land_area = ndb.FloatProperty()


    @classmethod
    def list_all(cls):
        return cls.query()
