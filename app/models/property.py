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
    # 1- SALE, 0 - RENT
    transaction_type = ndb.IntegerProperty(required=True)
    #profile_image = ndb.BlobKeyProperty(required=False)
    features = ndb.TextProperty(required=False, indexed=False)


    @classmethod
    def create(cls, params):
        item = cls(**params)
        item.put()
        return item

    @classmethod
    def update(cls, params):
        cls.populate(**params)
        cls.put()

    @classmethod
    def list_all(cls):
        return cls.query()

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
