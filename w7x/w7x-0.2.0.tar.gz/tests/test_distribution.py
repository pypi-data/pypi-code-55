import unittest
import w7x
import random
import numpy as np


class TestDistribution(unittest.TestCase):
    def test_sample_and_mean(self):
        d = w7x.batch.Distribution(random.randint, 0, 10)
        samples = [next(d) for i in range(100)]
        self.assertTrue(np.mean(samples) > 0 and np.mean(samples) < 10)

    def test_fixed_distribution(self):
        d = w7x.batch.Distribution(random.randint, 10, 10)
        samples = [next(d) for i in range(100)]
        self.assertTrue(samples == [10] * len(samples))


if __name__ == '__main__':
    unittest.main()
