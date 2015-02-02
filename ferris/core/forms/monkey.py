import wtforms.ext.appengine.ndb as wtfndb
import wtforms
from google.appengine.ext import ndb
from . import fields


### Additional Converters
def add_convertor(property_type, converter_func):
    setattr(wtfndb.ModelConverter, 'convert_%s' % property_type, converter_func)


def convert_UserProperty(self, model, prop, kwargs):
    """Returns a form field for a ``ndb.UserProperty``."""
    if isinstance(prop, ndb.Property) and (prop._auto_current_user or prop._auto_current_user_add):
        return None

    kwargs['validators'].append(wtforms.validators.email())
    kwargs['validators'].append(wtforms.validators.length(max=500))
    return fields.UserField(**kwargs)


def convert_KeyProperty(self, model, prop, kwargs):
    """Returns a form field for a ``ndb.KeyProperty``."""
    kwargs['kind'] = prop._kind
    kwargs.setdefault('allow_blank', not prop._required)
    if not prop._repeated:
        return fields.KeyPropertyField(**kwargs)
    else:
        del kwargs['allow_blank']
        return fields.MultipleReferenceField(**kwargs)


def convert_BlobKeyProperty(self, model, prop, kwargs):
    """Returns a form field for a ``ndb.BlobKeyProperty``."""
    return fields.BlobKeyField(**kwargs)


def convert_GeoPtProperty(self, model, prop, kwargs):
        return fields.GeoPtPropertyField(**kwargs)


def fallback_converter(self, model, prop, kwargs):
    pass

setattr(wtfndb.ModelConverter, 'fallback_converter', fallback_converter)

# Monkey-patch wtf's converters
add_convertor('UserProperty', convert_UserProperty)
add_convertor('KeyProperty', convert_KeyProperty)
add_convertor('BlobKeyProperty', convert_BlobKeyProperty)
add_convertor('GeoPtProperty', convert_GeoPtProperty)
