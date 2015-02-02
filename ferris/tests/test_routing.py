import unittest
from ferrisnose import AppEngineWebTest
from ferris.core import routing
from ferris.core.controller import Controller, route


def std_decorator(f):
    def std_wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return std_wrapper


class TestClass(Controller):
    class Meta:
        prefixes = ('pre',)

    def method1(self):
        pass

    def method2(self, arg1, arg2):
        pass

    def pre_method1(self):
        pass

    def pre_method2(self, arg1, arg2):
        pass

    @route
    def yuri(self):
        assert self.on_uri(action='yuri')
        assert not self.on_uri(action='list')

        if 'meow' in self.request.params:
            assert self.on_uri(meow='kitty')
            assert not self.on_uri(meow='dog')

        return 'success'

    @route
    @std_decorator
    def broken(self, meow, kitty):
        return 'success'


class RoutingTest(unittest.TestCase):

    def testPartsFromMethod(self):

        self.assertEquals(
            routing.canonical_parts_from_method(TestClass, TestClass.method1),
            {
                'prefix': None,
                'controller': 'test_class',
                'action': 'method1',
                'args': []
            }
        )

        self.assertEquals(
            routing.canonical_parts_from_method(TestClass, TestClass.method2),
            {
                'prefix': None,
                'controller': 'test_class',
                'action': 'method2',
                'args': ['arg1', 'arg2']
            }
        )

        self.assertEquals(
            routing.canonical_parts_from_method(TestClass, TestClass.pre_method1),
            {
                'prefix': 'pre',
                'controller': 'test_class',
                'action': 'method1',
                'args': []
            }
        )

        self.assertEquals(
            routing.canonical_parts_from_method(TestClass, TestClass.pre_method2),
            {
                'prefix': 'pre',
                'controller': 'test_class',
                'action': 'method2',
                'args': ['arg1', 'arg2']
            }
        )

        self.assertEquals(
            routing.canonical_parts_from_method(TestClass, TestClass.broken),
            {
                'prefix': None,
                'controller': 'test_class',
                'action': 'broken',
                'args': ['meow', 'kitty']
            }
        )

    def testPathFromParts(self):

        self.assertEquals(
            routing.path_from_canonical_parts(None, 'one', 'two', []),
            '/one/two'
        )

        self.assertEquals(
            routing.path_from_canonical_parts('pre', 'one', 'two', []),
            '/pre/one/two'
        )

        self.assertEquals(
            routing.path_from_canonical_parts(None, 'one', 'two', ['x', 'y']),
            '/one/two/<x>/<y>'
        )

        self.assertEquals(
            routing.path_from_canonical_parts('pre', 'one', 'two', ['x', 'y']),
            '/pre/one/two/<x>/<y>'
        )

    def testNameFromParts(self):

        self.assertEquals(
            routing.name_from_canonical_parts(None, 'one', 'two', []),
            'one:two'
        )

        self.assertEquals(
            routing.name_from_canonical_parts('pre', 'one', 'two', []),
            'pre:one:two'
        )

        self.assertEquals(
            routing.name_from_canonical_parts(None, 'one', 'two', ['x', 'y']),
            'one:two'
        )

        self.assertEquals(
            routing.name_from_canonical_parts('pre', 'one', 'two', ['x', 'y']),
            'pre:one:two'
        )


class TestOnUri(AppEngineWebTest):
    def setUp(self):
        super(TestOnUri, self).setUp()
        self.addController(TestClass)

    def testOnUri(self):
        self.testapp.get('/test_class/yuri')
        self.testapp.get('/test_class/yuri?meow=kitty')
