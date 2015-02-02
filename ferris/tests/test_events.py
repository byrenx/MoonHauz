import unittest
from ferris.core.event import Event, NamedEvents
from ferris.core import events


class EventTest(unittest.TestCase):

    def testEvent(self):
        event = Event()
        called_list = []

        def test_listener(x):
            called_list.append(x)

        event += test_listener
        event(True)

        self.assertTrue(True in called_list)

        # test getHandlerCount
        data = event.getHandlerCount()
        self.assertEqual(1, data)

        del called_list[:]

        event -= test_listener
        event.fire(True)
        self.assertTrue(True not in called_list)

        self.assertRaises(ValueError, event.unhandle, test_listener)  # test lines 35-36


class NamedEventsTest(unittest.TestCase):

    def testNamedEvents(self):
        data = NamedEvents()

        temp = 'hello world'
        events.register(temp)

        called_list = []

        def test_listener_one(x):
            called_list.append(x)

        def test_listener_two(x):
            called_list.remove(x)

        data.add_item += test_listener_one
        data.remove_item += test_listener_two

        data.getEvent('fake')

        data.add_item(True)

        self.assertTrue(True in called_list)

        data.remove_item(True)

        self.assertTrue(True not in called_list)
