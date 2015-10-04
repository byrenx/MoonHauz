from google.appengine.ext.ndb import polymodel
from datetime import datetime, timedelta
from ferris import BasicModel, ndb, messages
from protopigeon.converters import Converter, KeyConverter, converters as default_converters
from protopigeon import to_message


class ReferenceToValueConverter(Converter):
    @staticmethod
    def to_message(Mode, property, field, value):
        return str(value.get())

    @staticmethod
    def to_field(Model, property, count):
        return messages.StringField(count, repeated=property._repeated)

key_converter = {'KeyProperty': ReferenceToValueConverter}

class Property(BasicModel, polymodel.PolyModel):
    name = ndb.StringProperty(required=True, indexed=True)
    location = ndb.StringProperty(required=True, indexed=True)
    sold = ndb.BooleanProperty(default=False)
    price = ndb.FloatProperty(required=True)
    # SALE, RENT
    transaction_type = ndb.StringProperty(required=True)
    #profile_image = ndb.BlobKeyProperty(required=False)
    features = ndb.TextProperty(required=False, indexed=False)
    geo_point = ndb.GeoPtProperty(required=False)
    images = ndb.BlobKeyProperty(repeated=True, required=False)
    documents = ndb.BlobKeyProperty(repeated=True, required=False)


    @classmethod
    def create(cls, params):
        params['geo_point'] = ndb.GeoPt(params['geo_point'])
        item = cls(**params)
        item.put()
        return item

    @classmethod
    def to_message(cls, property):
        """
        (Property) --> PropertyMessage
        
        Retuns a Transformed Message of the Property to include
        all fields available based on Property type
        """
        return cls.buildProperty(property)

    @classmethod
    def update(cls, params):
        cls.populate(**params)
        cls.put()
      
    @classmethod
    def list_all(cls):
        properties = [cls.buildProperty(p) for p in cls.query().fetch()]
        return PropertiesMessage(properties = properties)

    @classmethod
    def list_by_location(cls, location):
        return cls.query(cls.location >= location).order(cls.location)
    
    @classmethod
    def buildProperty(cls, property):
        return PropertyMessage(type =  cls.identify_type(property._class_name()),
                               key = property.key.urlsafe(),
                               name = property.name,
                               location = property.location,
                               price = property.price,
                               features = property.features,
                               transaction_type = property.transaction_type,
                               sold = property.sold,
                               geo_point = GeoPtMessage(lat=property.geo_point.lat, lon = property.geo_point.lon),
                               land_area = property.land_area if property._class_name() == 'Land' or property._class_name() == 'HouseAndLot' else None,
                               land_type = property.land_type if property._class_name() == 'Land' else None,
                               floors = property.floors if property._class_name() == 'HouseAndLot' else None,
                               bedrooms = property.bedrooms if property._class_name() == 'HouseAndLot' else None,
                               floor_area = property.floor_area if property._class_name() == 'HouseAndLot' else None                               
                           )

    @classmethod
    def identify_type(cls, type):
        if type == 'Land':
            return 'Land'
        elif type == 'HouseAndLot':
            return 'House and Lot'
        elif type == 'CondoUnit':
            return 'Condo'

    @classmethod
    def list_by_for_sale(cls):
        return cls.query(cls.transaction_type == 1)

    @classmethod
    def list_by_for_rent(cls):
        return cls.query(cls.transaction_type == 0)

    @classmethod
    def list_by_sold(cls):
        return cls.query(cls.sold == True)

    @classmethod
    def list_by_for_unsold(cls):
        return cls.query(cls.sold == False)

    '''messages configs'''

    @classmethod
    def message_props(cls, only=None, exclude=None, converters=None):
        props = cls._properties
        sorted_props = sorted(props.iteritems(), key=lambda prop: prop[1]._creation_counter)
        field_names = [x[0] for x in sorted_props if x[0]]
        if exclude:
            field_names = [x for x in field_names if x not in exclude]
        if only:
            field_names = [x for x in field_names if x in only]
        converters = dict(default_converters.items() + converters.items()) if converters else default_converters
        key_holder = type('', (), {})()
        key_holder.name = 'key',
        key_holder._repeated = False
        field_dict = {
            'key': converters['Key'].to_field(cls, key_holder, 1)
        }
        last_count = 0
        for count, name in enumerate(field_names, start=2):
            last_count = count
            prop = props[name]
            converter = converters.get(prop.__class__.__name__, None)
            if converter:
                field_dict[name] = converter.to_field(cls, prop, count)
        return field_dict, last_count

    @classmethod
    def message(cls):
        field_dict, count = cls.message_props(converters=key_converter)
        return type('car', (messages.Message,), field_dict)

    @staticmethod
    def car_message(entity, message):
        ret = messages.to_message(entity, message)
        return ret


class GeoPtMessage(messages.Message):
    lat = messages.FloatField(1)
    lon = messages.FloatField(2)


class PropertyMessage(messages.Message):
    type = messages.StringField(1)
    key = messages.StringField(2)
    name = messages.StringField(3)
    location = messages.StringField(4)
    price = messages.FloatField(5)
    features = messages.StringField(6)
    transaction_type = messages.StringField(7)
    sold = messages.BooleanField(8)
    geo_point = messages.MessageField(GeoPtMessage, 9)
    land_area = messages.FloatField(10)
    land_type = messages.StringField(11)
    floors = messages.IntegerField(12)
    bedrooms = messages.IntegerField(13)
    floor_area = messages.FloatField(14)



class PropertiesMessage(messages.Message):
    properties = messages.MessageField(PropertyMessage, 1, repeated=True)
