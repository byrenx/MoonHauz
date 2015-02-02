from ferrisnose import AppEngineWebTest
from ferris.core.controller import Controller, route
from ferris.components import edge_cache


class Cachable(Controller):
    class Meta:
        components = (edge_cache.EdgeCache,)

    @route
    def public(self):
        self.components.edge_cache('public')
        return 'public'

    @route
    def private(self):
        self.components.edge_cache('private')
        return 'private'

    @route
    @edge_cache.set('public')
    def decorator(self):
        return 'decorator'


class TestEdgeCaching(AppEngineWebTest):
    def setUp(self):
        super(TestEdgeCaching, self).setUp()
        Cachable._build_routes(self.testapp.app.router)

    def test(self):
        r = self.testapp.get('/cachable/public')
        assert r.headers['Cache-Control'] == 'max-age=900, public'

        r = self.testapp.get('/cachable/private')
        assert r.headers['Cache-Control'] == 'max-age=900, private'

        r = self.testapp.get('/cachable/decorator')
        assert r.headers['Cache-Control'] == 'max-age=900, public'
