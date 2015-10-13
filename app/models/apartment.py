from ferris import BasicModel, ndb
from app.models.property import Property

class Apartment(Property):
    bedrooms = ndb.IntegerProperty()
    floor_area = ndb.FloatProperty()

    @classmethod
    def list_all(cls):
        return cls.query()
    
