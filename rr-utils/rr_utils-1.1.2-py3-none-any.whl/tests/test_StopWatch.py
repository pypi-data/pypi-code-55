import time
from unittest import TestCase

from StopWatch.StopWatch import StopWatch


class TestStopWatch(TestCase):
    def test_case1(self):
        obj = StopWatch()
        self.assertLess(time.time() - obj.get_start_time(), 0.1)
        self.assertLess(obj.get_elapsed_time(), 0.1)
        time.sleep(0.5)
        self.assertLess(obj.get_elapsed_time(), 0.6)
        self.assertGreater(obj.get_elapsed_time(), 0.45)
        obj.reset()
        self.assertLess(obj.get_elapsed_time(), 0.1)

    def test_case2(self):
        obj = StopWatch(auto_start=False)
        self.assertIsNone(obj.get_start_time())
        self.assertIsNone(obj.get_elapsed_time())
        time.sleep(0.2)

        with obj as timer:
            time.sleep(0.5)

        time.sleep(0.2)

        self.assertLess(obj.get_elapsed_time(), 0.6)
        self.assertGreater(obj.get_elapsed_time(), 0.45)
