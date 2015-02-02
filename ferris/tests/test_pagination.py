from ferrisnose import AppEngineWebTest
from ferris.core import scaffold
from ferris.core.controller import Controller, route
from ferris.core.ndb import Model, ndb
from ferris.components import pagination, search
from ferris.behaviors import searchable
from ferris.core import messages


class Sprocket(Model):
    class Meta:
        behaviors = (searchable.Searchable,)

    stamp = ndb.IntegerProperty()
    name = ndb.StringProperty()


class Sprockets(Controller):
    class Meta:
        prefixes = ('api',)
        components = (scaffold.Scaffolding, pagination.Pagination, messages.Messaging, search.Search)
        pagination_limit = 10
        Model = Sprocket

    list = scaffold.list
    api_list = scaffold.list

    @route
    def api_search(self):
        self.components.search(sort_field='stamp', sort_direction='asc')


class TestPagination(AppEngineWebTest):
    def setUp(self):
        super(TestPagination, self).setUp()
        Sprockets._build_routes(self.testapp.app.router)

        # Create a few pages of sprokets
        for i in range(1, 50):
            Sprocket(name=str(i), stamp=i).put()

    def testNormalList(self):
        r = self.testapp.get('/sprockets')
        assert '11' not in r

        _, cursor, _ = Sprocket.query().fetch_page(10)

        assert cursor
        r = self.testapp.get('/sprockets?cursor=%s' % cursor.urlsafe())
        assert '11' in r

    def testApiList(self):

        r = self.testapp.get('/api/sprockets')
        assert '10' in r
        assert '11' not in r

        assert len(r.json['items']) == 10
        assert r.json['count'] == 10
        assert r.json['limit'] == 10
        assert r.json['next_page']
        assert r.json['page'] == 1
        assert 'previous_page' not in r.json

        r = self.testapp.get(r.json['next_page'])
        assert '11' in r
        assert 'previous_page' in r.json
        assert r.json['page'] == 2

    def testSearchList(self):
        r = self.testapp.get('/api/sprockets/search')
        assert '10' in r

        assert len(r.json['items']) == 10
        assert r.json['count'] == 10
        assert r.json['limit'] == 10
        assert r.json['next_page']

        r = self.testapp.get(r.json['next_page'])
        print [x['name'] for x in r.json['items']]
        assert '11' in r
