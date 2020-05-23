import unittest
import CallOnce

counter = 0


class TestsNestedFunction(unittest.TestCase):
    def test_no_cache(self):
        @CallOnce.CallOnce()
        def func_nested(arg):
            """description"""
            global counter
            counter += 1
            return arg * arg

        global counter
        local_counter = counter

        result = func_nested(10)
        self.assertEqual(counter, local_counter + 1)
        self.assertEqual(result, 100)

        result = func_nested(2)
        self.assertEqual(counter, local_counter + 1)
        self.assertEqual(result, 100)

        self.assertEqual("func_nested", func_nested.__name__)
        self.assertEqual("description", func_nested.__doc__)


if __name__ == '__main__':
    unittest.main()

