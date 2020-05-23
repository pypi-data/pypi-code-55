import unittest
from datetime import timedelta
import CallOnce

counter = 0


@CallOnce.CallOnce(ttl=timedelta(milliseconds=100))
def func1(arg):
    """description"""
    global counter
    counter += 1
    return arg * arg


class TestsFreeFunction(unittest.TestCase):

    def test_ttl(self):
        global counter
        local_counter = counter
        result = func1(10)
        self.assertEqual(result, 100)
        self.assertEqual(counter, local_counter + 1)
        func1(2)
        self.assertEqual(counter, local_counter + 1)
        func1(2)
        self.assertEqual(counter, local_counter + 1)
        func1(2)
        self.assertEqual(counter, local_counter + 1)

        from time import sleep
        sleep(0.5)
        func1(2)
        self.assertEqual(counter, local_counter + 2)


if __name__ == '__main__':
    unittest.main()
