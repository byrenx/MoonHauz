from ferrisnose import AppEngineWebTest
from ferris.core.controller import Controller
from ferris.core.messages import Messaging
from ferris.core.ndb import Model, ndb
import json


class Person(Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty()


class People(Controller):
    class Meta:
        Model = Person
        components = (Messaging,)
        prefixes = ('api',)

    def api_list(self):
        self.context['data'] = Person.query()

    def api_view(self, key):
        self.context['data'] = self.util.decode_key(key).get()

    def api_add(self):
        result = self.parse_request()
        if result.validate():
            item = result.update(Person)
            item.put()
            self.context['data'] = item
        else:
            self.context['errors'] = result.errors
            return 400

    def api_edit(self, key):
        item = self.util.decode_key(key).get()
        result = self.parse_request()
        if item and result.validate():
            item = result.update(item)
            item.put()
            self.context['data'] = item
        else:
            self.context['errors'] = result.errors
            return 400


class MessagingTest(AppEngineWebTest):
    def setUp(self):
        super(MessagingTest, self).setUp()
        People._build_routes(self.testapp.app.router)
        self._createData()

    def _createData(self):
        Person(title='The Doctor', content='Time Lord').put()
        Person(title='Rose Tyler', content='Companion').put()
        Person(title='Clara Oswald', content='Mystery').put()

    def testList(self):
        response = self.testapp.get('/api/people')

        assert response.content_type == 'application/json'
        data = json.loads(response.body)

        assert 'items' in data
        assert len(data['items']) == Person.query().count()
        assert 'title' in data['items'][0]
        assert 'content' in data['items'][0]
        assert 'key' in data['items'][0]

    def testView(self):
        item = Person.query().get()
        response = self.testapp.get('/api/people/:%s' % item.key.urlsafe())

        assert response.content_type == 'application/json'
        data = json.loads(response.body)

        assert data['title'] == item.title
        assert data['content'] == item.content
        assert data['key']['urlsafe'] == item.key.urlsafe()

    def testAdd(self):
        data = json.dumps({'title': 'Dalek', 'content': 'Exterminate!'})

        response = self.testapp.post('/api/people', data, content_type='application/json')

        assert response.content_type == 'application/json'
        data = json.loads(response.body)

        assert data['title'] == 'Dalek'

        item = ndb.Key(urlsafe=data['key']['urlsafe']).get()

        assert item
        assert item.title == data['title']
        assert item.content == data['content']

    def testEdit(self):
        item = Person.query().get()
        data = json.dumps({'title': 'Captain Jack'})

        response = self.testapp.put('/api/people/:%s' % item.key.urlsafe(), data, content_type='application/json')

        assert response.content_type == 'application/json'
        data = json.loads(response.body)

        new_item = ndb.Key(urlsafe=data['key']['urlsafe']).get()

        assert new_item
        assert new_item.key == item.key
        assert new_item.content == item.content
        assert new_item.title == 'Captain Jack'

    def testErrors(self):
        data = json.dumps({'title': 'Dalek', 'content': 12346})

        r = self.testapp.post('/api/people', data, status=400, content_type='application/json')

        assert len(r.json['errors']) == 1
