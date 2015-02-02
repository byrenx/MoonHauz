from ferrisnose import AppEngineWebTest
from ferris.core import scaffold
from ferris.core.controller import Controller, route
from ferris.core.ndb import Model, ndb


class Widget(Model):
    name = ndb.StringProperty()


class Widgets(Controller):
    class Meta:
        prefixes = ('admin',)
        components = (scaffold.Scaffolding,)
        Model = Widget

    list = scaffold.list
    view = scaffold.view
    add = scaffold.add
    edit = scaffold.edit
    delete = scaffold.delete

    @route
    def list_alpha(self):
        def alpha_factory(self):
            return Widget.query().order(Widget.name)
        self.scaffold.query_factory = alpha_factory
        self.meta.change_view('json')
        return scaffold.list(self)

    @route
    def add_prefixed(self, prefix):
        def prefix_factory(self):
            return Widget(id=prefix)
        self.scaffold.create_factory = prefix_factory
        self.meta.change_view('json')
        self.scaffold.redirect = False
        return scaffold.add(self)


class TestScaffoldBehavior(AppEngineWebTest):
    def setUp(self):
        super(TestScaffoldBehavior, self).setUp()
        Widgets._build_routes(self.testapp.app.router)

    def testCrudMethods(self):
        self.testapp.get('/widgets/add')
        self.testapp.post('/widgets/add', {'name': 'Inigo Montoya'})
        self.assertEqual(Widget.query().count(), 1)

        r = self.testapp.get('/widgets')
        self.assertTrue('Inigo Montoya' in r)

        id = Widget.query().fetch(1)[0].key.urlsafe()

        r = self.testapp.get('/widgets/:%s' % id)
        self.assertTrue('Inigo Montoya' in r)

        r = self.testapp.get('/widgets/:%s/edit' % id)
        self.assertTrue('Inigo Montoya' in r)
        r.form['name'] = 'Dread Pirate Roberts'
        r = r.form.submit()

        r = self.testapp.get('/widgets/:%s' % id)
        self.assertTrue('Dread Pirate Roberts' in r)

        r = self.testapp.get('/widgets/:%s/delete' % id)
        self.assertEqual(Widget.query().count(), 0)

    def testRestMethods(self):
        self.testapp.post('/widgets', {'name': 'Inigo Montoya'})
        self.assertEqual(Widget.query().count(), 1)

        r = self.testapp.get('/widgets')
        self.assertTrue('Inigo Montoya' in r)

        id = Widget.query().fetch(1)[0].key.urlsafe()

        self.testapp.put('/widgets/:%s' % id, {'name': 'Dread Pirate Roberts'}, {'Content-type': 'application/x-www-form-urlencoded'})
        r = self.testapp.get('/widgets/:%s' % id)
        self.assertTrue('Dread Pirate Roberts' in r)

        r = self.testapp.delete('/widgets/:%s' % id)
        self.assertEqual(Widget.query().count(), 0)

    def testFactories(self):
        Widget(name='c').put()
        Widget(name='a').put()
        Widget(name='b').put()

        r = self.testapp.get('/widgets/list_alpha')

        assert r.json[0]['name'] == 'a'
        assert r.json[1]['name'] == 'b'
        assert r.json[2]['name'] == 'c'

        r = self.testapp.post('/widgets/add_prefixed/meow', {'name': 'dude'})

        assert r.json['name'] == 'dude'
        assert r.json['__id__'] == 'meow'
