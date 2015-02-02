import unittest


class MyTest(unittest.TestCase):

    def testMethod(self):
        self.assertEqual(1 + 2, 3, "1 + 2 not equal to 3")
