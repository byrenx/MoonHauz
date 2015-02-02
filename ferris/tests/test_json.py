from ferrisnose import AppEngineTest
from google.appengine.ext import db, ndb
from ferris.core.json_util import DatastoreEncoder, DatastoreDecoder
import datetime
import json


class NdbTestModel(ndb.Model):
    string = ndb.StringProperty()
    datetime = ndb.DateTimeProperty()  # auto_now_add=True is broken due to it calling now() locally instead of utcnow()
    person = ndb.UserProperty(auto_current_user=True)
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.TimeProperty()
    ref = ndb.KeyProperty()


class DbTestModel(db.Model):
    string = db.StringProperty()
    person = db.UserProperty(auto_current_user=True)
    ref = db.SelfReferenceProperty()


class JsonTest(AppEngineTest):

    def testNdbEncoding(self):
        # Key only test
        key = ndb.Key('RandomKind', 1)
        res = json.loads(json.dumps(key, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'ndb.Key')
        self.assertEqual(res['__key__'], key.urlsafe())
        self.assertEqual(res['__id__'], 1)

        # Keyless test
        ins = NdbTestModel(string='test', datetime=datetime.datetime.utcnow())

        res = json.loads(json.dumps(ins, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'ndb.Model')
        self.assertEqual(res['__key__'], None)
        self.assertEqual(res['__id__'], None)
        self.assertEqual(res['string'], 'test')
        self.assertEqual(res['person'], None)
        self.assertEqual(res['ref'], None)
        self.assertEqual(datetime.datetime.utcfromtimestamp(res['datetime']['timestamp']).utctimetuple(), ins.datetime.utctimetuple())

        # Keyed Test
        self.loginUser('test@test.com')
        ins.datetime = datetime.datetime.utcnow()
        ins.time = ins.datetime.time()
        ins.ref = ndb.Key('RandomKind', 1)
        ins.put()
        res = json.loads(json.dumps(ins, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'ndb.Model')
        self.assertEqual(res['__key__'], ins.key.urlsafe())
        self.assertEqual(res['__id__'], ins.key.id())
        self.assertEqual(res['string'], 'test')
        self.assertEqual(res['person']['email'], 'test@test.com')
        self.assertEqual(res['ref']['__class__'], 'ndb.Key')
        self.assertEqual(res['ref']['__key__'], ins.ref.urlsafe())
        self.assertEqual(res['ref']['__id__'], ins.ref.id())
        self.assertEqual(res['time']['hour'], ins.time.hour)
        self.assertEqual(res['time']['minute'], ins.time.minute)
        self.assertEqual(res['time']['second'], ins.time.second)
        self.assertEqual(res['time']['microsecond'], ins.time.microsecond)
        self.assertEqual(res['date']['year'], ins.date.year)
        self.assertEqual(res['date']['month'], ins.date.month)
        self.assertEqual(res['date']['day'], ins.date.day)
        self.assertEqual(datetime.datetime.utcfromtimestamp(res['datetime']['timestamp']).utctimetuple(), ins.datetime.utctimetuple())

        # Query test
        res = json.loads(json.dumps(NdbTestModel.query(), cls=DatastoreEncoder))
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0]['__key__'])

    def testDbEncoding(self):
        # Key only test
        key = db.Key.from_path('RandomKind', 1)
        res = json.loads(json.dumps(key, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'db.Key')
        self.assertEqual(res['__key__'], str(key))
        self.assertEqual(res['__id__'], 1)

        # Keyless Test
        ins = DbTestModel(string='test')

        res = json.loads(json.dumps(ins, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'db.Model')
        self.assertEqual(res['__key__'], None)
        self.assertEqual(res['__id__'], None)
        self.assertEqual(res['string'], 'test')
        self.assertEqual(res['person'], None)

        # Keyed test
        other = DbTestModel(string='other')
        other.put()

        self.loginUser('test@test.com')
        ins.ref = other
        ins.put()
        ins = DbTestModel.get(ins.key())
        res = json.loads(json.dumps(ins, cls=DatastoreEncoder))

        self.assertEqual(res['__class__'], 'db.Model')
        self.assertEqual(res['__key__'], str(ins.key()))
        self.assertEqual(res['__id__'], ins.key().id())
        self.assertEqual(res['string'], 'test')
        self.assertEqual(res['ref']['__class__'], 'db.Model')
        self.assertEqual(res['ref']['string'], 'other')

        # Query test
        res = json.loads(json.dumps(DbTestModel.all(), cls=DatastoreEncoder))
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2)
        self.assertTrue(res[0]['__key__'])

    def testNdbDecoding(self):
        # Keyless
        ins = NdbTestModel(string='test')
        ins.datetime = datetime.datetime(1990, 5, 29, 19, 8, 18)
        reprs = json.dumps(ins, cls=DatastoreEncoder)

        res = json.loads(reprs, cls=DatastoreDecoder)

        self.assertTrue(isinstance(res, NdbTestModel))
        self.assertEqual(res.key, None)
        self.assertEqual(res.string, 'test')
        self.assertEqual(res.datetime, ins.datetime)

        # with key
        self.loginUser("test@test.com")
        ins.ref = ndb.Key('RandomKind', 1)
        ins.put()
        reprs = json.dumps(ins, cls=DatastoreEncoder)

        res = json.loads(reprs, cls=DatastoreDecoder)

        self.assertTrue(isinstance(res, NdbTestModel))
        self.assertNotEqual(res.key, None)
        self.assertEqual(res.string, 'test')
        self.assertEqual(res.datetime, ins.datetime)
        self.assertEqual(res.date, ins.date)
        self.assertEqual(res.time, ins.time)
        self.assertEqual(res.person.email(), 'test@test.com')
        self.assertEqual(res.ref, ins.ref)
