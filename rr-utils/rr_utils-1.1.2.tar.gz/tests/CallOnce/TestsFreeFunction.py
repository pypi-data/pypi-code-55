import unittest

import CallOnce

counter = 0


@CallOnce.CallOnce()
def func1(arg):
    """description"""
    global counter
    counter += 1
    return arg * arg


@CallOnce.CallOnce()
def func2(arg):
    """description"""
    global counter
    counter += 1
    return arg * arg


class TestsFreeFunction(unittest.TestCase):

    def test_no_argument_cache(self):
        global counter
        local_counter = counter
        result = func1(10)
        self.assertEqual(result, 100)
        self.assertEqual(counter, local_counter + 1)
        result = func1(2)
        self.assertEqual(result, 100)
        self.assertEqual(counter, local_counter + 1)

        result = func2(3)
        self.assertEqual(result, 9)
        self.assertEqual(counter, local_counter + 2)

        result = func2(5)
        self.assertEqual(result, 9)
        self.assertEqual(counter, local_counter + 2)

        self.assertEqual("func1", func1.__name__)
        self.assertEqual("description", func1.__doc__)


if __name__ == '__main__':
    unittest.main()
