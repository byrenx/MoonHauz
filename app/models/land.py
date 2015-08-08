#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

from app.models.property import Property

class Land(Property):
    # RESIDENTIAL ,COMMERCIAL, AGRICULTURE
    land_type = ndb.StringProperty(required=False)
    land_area = ndb.FloatProperty(required=False)

        
