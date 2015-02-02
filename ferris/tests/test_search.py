from ferrisnose import AppEngineTest
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import search as search_api
from ferris.core import search
import datetime


class SearchTestModel(ndb.Model):
    string = ndb.StringProperty()
    string2 = ndb.StringProperty()
    repeated_string = ndb.StringProperty(repeated=True)
    datetime = ndb.DateTimeProperty()  # auto_now_add=True is broken due to it calling now() locally instead of utcnow()
    person = ndb.UserProperty(auto_current_user=True)
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.TimeProperty()
    ref = ndb.KeyProperty()
    geopt = ndb.GeoPtProperty()
    repeated_number = ndb.IntegerProperty(repeated=True)


class SearchTest(AppEngineTest):

    def _create_test_data(self):
        instance = SearchTestModel(
            string='123',
            repeated_string=['1', '2', '3'],
            datetime=datetime.datetime.utcnow(),
            person=users.User(email='a@example.com'),
            date=datetime.date.today(),
            time=datetime.time(4),
            ref=ndb.Key('Test', '123'),
            geopt=ndb.GeoPt(1, 2),
            repeated_number=[1, 2, 3])
        instance.put()
        return instance

    def test_indexer(self):
        instance = self._create_test_data()

        indexed_fields = search.default_entity_indexer(instance, instance._properties.keys())

        assert len(indexed_fields) == 10  # -1 for the key, +1 for the datetime (creates two fields), +3 for the repeated string

    def test_index_and_unindex(self):
        instance = self._create_test_data()
        search_index = search_api.Index(name='test_index')

        search.index_entity(instance, index='test_index')

        response = search_index.get_range()
        assert len(response.results) == 1

        search.unindex_entity(instance, index='test_index')

        response = search_index.get_range()
        assert len(response.results) == 0

    def test_search(self):
        instance = self._create_test_data()
        search.index_entity(instance, index='test_index')

        error, results, current_cursor, next_cursor = search.search('test_index', '')

        assert not error
        assert len(results) == 1
