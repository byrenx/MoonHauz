#python libraries
from datetime import datetime, timedelta
#ferris linraries
from ferris import BasicModel, ndb

class Property(BasicModel, polymodel.PolyModel):
    name = ndb.StringProperty(required=True, indexed=True)
    location = ndb.StringProperty(required=True, indexed=True)
    area_in_sqm = ndb.FloatProperty()
    sold = ndb.BooleanProperty(default=False)
    price = ndb.FloatProperty(required=True)
    #profile_image = ndb.BlobKeyProperty(required=False)
    freatures = ndb.TextProperty(required=False, indexed=False)


    @classmethod
    def create(cls, params):
        item = cls(**params)
        item.put()
        return item

    @classmethod
    def update(cls, params):
        cls.populate(**params)
        cls.put()

    @clasmethod
    def list_all(cls):
        return cls.query()

    
