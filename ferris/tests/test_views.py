from ferrisnose import AppEngineWebTest
from ferris.core.controller import Controller, route
from ferris.core.views import ViewContext, View, JsonView


class Widgets(Controller):

    @route
    def json(self):
        self.meta.change_view('Json')
        self.context['data'] = {'one': 2}

    @route
    def template(self):
        self.meta.change_view('Template')
        self.meta.view.template_name = 'index.html'


class TestJsonView(AppEngineWebTest):
    def setUp(self):
        super(TestJsonView, self).setUp()
        self.addController(Widgets)

    def testViewContext(self):
        ctx = ViewContext()
        ctx.set_dotted('cat.name', 'Fluffly')
        assert ctx.get_dotted('cat.name') == 'Fluffly'

    def testBaseView(self):
        v = View(object(), {'meow': 'one'})
        assert isinstance(v.context, ViewContext)

        self.assertRaises(NotImplementedError, v.render)

    def testJsonView(self):
        v = JsonView(object())
        assert v._get_data('meow') == 'meow'

        r = self.testapp.get('/widgets/json')
        print r
        assert r.json['one'] == 2

    def testTemplateView(self):
        self.testapp.get('/widgets/template')
