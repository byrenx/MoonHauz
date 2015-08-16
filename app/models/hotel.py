#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class Hotel(Property):
    floors = ndb.IntegerProperty(required=True, default=1)
    floor_area = ndb.FloatProperty()
    land_area = ndb.FloatProperty()
    rooms = ndb.IntegerProperty()
