import unittest
import CallOnce

counter = 0


class TestsInSelfMethod(unittest.TestCase):
    @CallOnce.CallOnce()
    def _method(self, arg):
        """description"""
        global counter
        counter += 1
        return arg * arg

    def test_no_argument_cache(self):
        result = self._method(10)
        self.assertEqual(result, 100)

        result = self._method(2)
        self.assertEqual(result, 100)

        # todo: implement missing part

        self.assertEqual(self._method.__name__, "_method")
        self.assertEqual(self._method.__doc__, "description")


if __name__ == '__main__':
    unittest.main()

