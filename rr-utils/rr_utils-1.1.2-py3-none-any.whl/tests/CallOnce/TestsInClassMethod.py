import unittest
import CallOnce

counter = 0


class Helper:
    @CallOnce.CallOnce()
    def method(self, arg):
        """description"""
        global counter
        counter += 1
        return arg * arg


class TestsNestedFunction(unittest.TestCase):
    def test_no_argument_cache(self):
        global counter
        local_counter = counter
        obj1 = Helper()
        obj2 = Helper()

        result = obj1.method(1)
        self.assertEqual(counter, local_counter + 1)
        self.assertEqual(result, 1)

        result = obj1.method(14)
        self.assertEqual(counter, local_counter + 1)
        self.assertEqual(result, 1)

        self.assertEqual("method", obj1.method.__name__)
        self.assertEqual("description", obj1.method.__doc__)

        result = obj2.method(3)
        self.assertEqual(counter, local_counter + 2)
        self.assertEqual(result, 9)

        result = obj2.method(14)
        self.assertEqual(counter, local_counter + 2)
        self.assertEqual(result, 9)

        self.assertEqual("method", obj2.method.__name__)
        self.assertEqual("description", obj2.method.__doc__)


if __name__ == '__main__':
    unittest.main()

