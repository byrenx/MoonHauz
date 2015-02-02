from ferrisnose import AppEngineWebTest
import wtforms
import json
from ferris.core.controller import Controller, route, route_with
from ferris.core.json_util import DatastoreEncoder
from google.appengine.ext import ndb


# Decorators that make sure @route works correctly even for decorated functions
def std_decorator(f):
    def std_wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return std_wrapper


def wraps_decorator(f):
    from functools import wraps

    @wraps(f)
    def wraps_wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wraps_wrapper


class TestModel(ndb.Model):
    field1 = ndb.StringProperty()
    field2 = ndb.StringProperty()


class TestForm(wtforms.Form):
    field1 = wtforms.TextField()
    field2 = wtforms.TextField()


class TestComponent(object):
    def __init__(self, handler):
        self.handler = handler

    def present(self):
        return 'si'


class TestController(Controller):
    class Meta:
        prefixes = ('monster',)
        components = (TestComponent,)

    def list(self):
        return 'list'

    def view(self, key):
        return 'view'

    def add(self):
        return 'add'

    def edit(self, key):
        return 'edit'

    def delete(self, key):
        return 204

    def monster_list(self):
        return 'monster_list'

    @route
    @wraps_decorator
    def monkey(self, key):
        return 'monkey-%s' % key

    @route
    @std_decorator
    def monster_monkey(self, key):
        return 'monster_monkey-%s' % key

    @route_with('/test_controller/monet')
    def degas(self):
        return 'degas'

    @route
    def urls(self):
        assert self.uri(action='list') == '/test_controller'
        assert self.uri(prefix='monster', action='list') == '/monster/test_controller'
        assert self.uri(action='edit', key=12) == '/test_controller/%3A12/edit'
        assert self.uri('test_controller:list') == '/test_controller'
        assert self.uri('monster:test_controller:list') == '/monster/test_controller'
        assert self.uri('test_controller:monkey', key=13) == '/test_controller/monkey/13'

        return 'success'

    @route
    def component(self):
        return self.components.test_component.present()

    @route
    def numeric(self):
        return 401

    @route
    def custom_content(self):
        self.response.content_type = 'application/json'
        return '[1, 2, 3]'

    @route
    def self_response(self):
        self.response.status_int = 401
        self.response.body = 'lolidk'
        return self.response

    @route
    def do_redirect(self):
        return self.redirect(self.uri('test_controller:list'))

    @route
    def monster_template_names(self):
        return str(self.meta.view.get_template_names())

    @route
    def form(self):
        form = TestForm()
        self.parse_request(container=form)
        return str(form.data)


class ControllerTest(AppEngineWebTest):
    def setUp(self):
        super(ControllerTest, self).setUp()
        TestController._build_routes(self.testapp.app.router)

    def testCrudRoutes(self):
        response = self.testapp.get('/test_controller')
        self.assertEqual(response.body, 'list')

        response = self.testapp.get('/test_controller/add')
        self.assertEqual(response.body, 'add')

        response = self.testapp.get('/test_controller/:abcd')
        self.assertEqual(response.body, 'view')

        response = self.testapp.get('/test_controller/:abcd/edit')
        self.assertEqual(response.body, 'edit')

        response = self.testapp.get('/test_controller/:abcd/delete', status=204)

    def testRestRoutes(self):
        response = self.testapp.get('/test_controller')
        self.assertEqual(response.body, 'list')

        response = self.testapp.post('/test_controller')
        self.assertEqual(response.body, 'add')

        response = self.testapp.get('/test_controller/:abcd')
        self.assertEqual(response.body, 'view')

        response = self.testapp.put('/test_controller/:abcd')
        self.assertEqual(response.body, 'edit')

        response = self.testapp.delete('/test_controller/:abcd', status=204)

    def testPrefixRoutes(self):
        response = self.testapp.get('/monster/test_controller')
        self.assertEqual(response.body, 'monster_list')

    def testRouteDecorator(self):
        response = self.testapp.get('/test_controller/monkey/3')
        self.assertEqual(response.body, 'monkey-3')

        response = self.testapp.get('/monster/test_controller/monkey/3')
        self.assertEqual(response.body, 'monster_monkey-3')

    def testRouteWithDecorator(self):
        response = self.testapp.get('/test_controller/monet')
        self.assertEqual(response.body, 'degas')

    def testUrlGeneration(self):
        response = self.testapp.get('/test_controller/urls')
        self.assertEqual(response.body, 'success')

    def testComponents(self):
        response = self.testapp.get('/test_controller/component')
        self.assertEqual(response.body, 'si')

    def testReturnValues(self):
        response = self.testapp.get('/test_controller')
        assert 'text/html' in response.headers['Content-Type']
        self.assertEqual(response.body, 'list')

        response = self.testapp.get('/test_controller/numeric', status=401)

        response = self.testapp.get('/test_controller/custom_content', status=200)
        assert 'application/json' in response.headers['Content-Type']

        response = self.testapp.get('/test_controller/self_response', status=401)
        self.assertEqual(response.body, 'lolidk')

        response = self.testapp.get('/test_controller/do_redirect', status=302)
        self.assertEqual(response.headers['Location'], 'http://localhost/test_controller')

    def testTemplateNames(self):
        response = self.testapp.get('/monster/test_controller/template_names')
        self.assertEqual(response.body, str(['test_controller/monster_template_names.html', 'test_controller/template_names.html']))

    def testFormDataProcessor(self):
        data = {'field2': u'f2', 'field1': u'f1'}
        response = self.testapp.post('/test_controller/form', data)
        self.assertEqual(response.body, str(data))

        data['field3'] = u'f3'
        response = self.testapp.post('/test_controller/form', data)
        self.assertNotEqual(response.body, str(data), 'Field3 should not be in data')

        del data['field3']
        data = json.dumps(data, cls=DatastoreEncoder)

        response = self.testapp.post('/test_controller/form', data, headers={'Content-Type': 'application/json'})
        self.assertTrue('f1' in response)
        self.assertTrue('f2' in response)
