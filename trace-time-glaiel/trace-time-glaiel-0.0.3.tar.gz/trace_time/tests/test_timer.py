import unittest
from trace_time.timer import Timer
import time


class TestBasicFunction(unittest.TestCase):

    def test_time(self):
        self.assertAlmostEqual(time.time(), Timer()._origin, delta=0.01)

    def test_tic_toc(self):
        pause = 1.2
        timer = Timer()
        timer.tic("t0")
        time.sleep(pause)
        timer.toc("t0")
        self.assertAlmostEqual(timer.get_elapsed("t0"), pause, delta=0.01)


if __name__ == '__main__':
    unittest.main()
