#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class HouseAndLot(Property):
    floors = ndb.IntegerProperty(require=True)
    bedrooms = ndb.IntegerProperty(require=True)
