#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class CondoUnit(Property):
    capacity = ndb.IntegerProperty(required=True)
    bedrooms = ndb.IntegerProperty(require=True)
