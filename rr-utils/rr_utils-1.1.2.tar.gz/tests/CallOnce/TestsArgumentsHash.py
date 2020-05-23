import unittest

import CallOnce
from CallOnce.Enums import ArgumentsMode, HashFunction


counter = 0


def base_func(arg1, arg2, arg3):
    global counter
    counter += 1
    return "{}{}{}".format(arg1, arg2, arg3)


@CallOnce.CallOnce(args_mode=ArgumentsMode.SERIALIZE_AND_HASH, hash_mode=HashFunction.PYTHON)
def func1(*args):
    return base_func(*args)


@CallOnce.CallOnce(args_mode=ArgumentsMode.SERIALIZE_AND_HASH, hash_mode=HashFunction.MD5)
def func2(*args):
    return base_func(*args)


class TestsArgumentsHash(unittest.TestCase):

    def _test_single_case(self, f, args, should_execute):
        global counter
        local_counter = counter
        arg1, arg2, arg3 = args
        result = f(arg1, arg2, arg3)

        if should_execute:
            expected_result = "{}{}{}".format(arg1, arg2, arg3)
            self.assertEqual(expected_result, result)
            self.assertEqual(counter, local_counter + 1)
        else:
            self.assertEqual(counter, local_counter)

    def _make_test(self, args):
        for f in [func1, func2]:
            self._test_single_case(f, args, True)
            self._test_single_case(f, args, False)

    def test_values(self):
        self._make_test([1, 1, 1])
        self._make_test([1, 2, 3])
        self._make_test([1, 2, 2])

        self._make_test([1, 2, 0])
        self._make_test([1, 2, False])
        self._make_test([1, 2, None])
        self._make_test([1, 0, 2])
        self._make_test([0, 2, 1])
        self._make_test([0, 1, 2])

    def test_list_and_tuple(self):
        self._make_test([[], 0, 0])
        self._make_test([(), 0, 0])
        self._make_test([(1,), 0, 0])
        self._make_test([0, (), 0])
        self._make_test([0, [], 0])
        self._make_test([0, [None], 0])
        self._make_test([0, [], []])
        self._make_test([0, [], ()])

        self._make_test(["fffff", [], 0])
        self._make_test([[], [], []])
        self._make_test([0, [4], 0])
        self._make_test([0, [4, 4], 0])
        self._make_test([0, [4, 4, 4], 0])
        self._make_test([[4, 4, 4], [4, 4, 4], [4, 4, 4]])
        self._make_test([[4, 4, 4], [4, 4, 4], [4, 4, 3]])

    def test_dic(self):
        self._make_test([{}, 0, 0])
        self._make_test([{}, {}, 0])
        self._make_test([0, {}, 0])
        self._make_test([0, 0, {}])
        self._make_test([{1: "a"}, 0, 0])
        self._make_test([{1: "b"}, 0, 0])
        self._make_test([{2: "a"}, 0, 0])
        self._make_test([{2: {}}, 0, 0])
        self._make_test([0, {1: "a"}, 0])


if __name__ == '__main__':
    unittest.main()
