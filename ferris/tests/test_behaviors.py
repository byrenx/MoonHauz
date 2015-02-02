from ferrisnose import AppEngineTest
from ferris.core.ndb import Model, Behavior, ndb


class TestBehavior(Behavior):
    count = 0
    deleted_count = 0

    def before_put(self, instance):
        instance.string_two = instance.string_one + '4'

    def after_put(self, instance):
        TestBehavior.count += 1

    def before_get(self, key):
        TestBehavior.count += 1

    def after_get(self, instance):
        instance.string_one += 'meow'

    def before_delete(self, key):
        TestBehavior.count -= 1

    def after_delete(self, key):
        TestBehavior.deleted_count += 1


class BehaviorTestModel(Model):
    class Meta:
        behaviors = (TestBehavior,)

    string_one = ndb.StringProperty()
    string_two = ndb.StringProperty()


class BehaviorTest(AppEngineTest):

    def test(self):
        m = BehaviorTestModel(string_one='123')
        m.put()

        assert m.string_two == '1234'
        assert TestBehavior.count == 1

        m2 = m.key.get()

        assert 'meow' in m2.string_one
        assert TestBehavior.count == 2

        m.key.delete()

        assert TestBehavior.count == 1
        assert TestBehavior.deleted_count == 1
