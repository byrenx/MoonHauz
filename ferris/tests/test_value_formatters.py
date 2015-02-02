from ferrisnose import AppEngineTest
from google.appengine.ext import ndb
from ferris.core.template import format_value
import datetime


class FormatTestModel(ndb.Model):
    name = ndb.StringProperty()

    def __unicode__(self):
        return self.name or u"Un-named"


class ValueFormatterTest(AppEngineTest):

    def test_string_types(self):
        assert format_value("test") == "test"
        assert format_value(u"test") == u"test"
        assert format_value(["test", "1", "2"]) == u"test, 1, 2"
        assert format_value([u"test", u"1", u"2"]) == u"test, 1, 2"

    def test_datastore_types(self):
        ins = FormatTestModel(name=u"Meow")
        assert format_value(ins) == u"Meow"

        key = ins.put()
        assert format_value(key) == u"Meow"

        ins2 = FormatTestModel(name=u"Woof")
        assert format_value([ins, ins2]) == u"Meow, Woof"

        key2 = ins2.put()
        assert format_value([key, key2]) == u"Meow, Woof"
