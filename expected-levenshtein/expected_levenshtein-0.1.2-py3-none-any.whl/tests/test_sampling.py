#!/usr/bin/env python

import unittest
import numpy as np
import expected_levenshtein.sample as sample


class TestLevenshteinSamplingFunctions(unittest.TestCase):
    def test_lev(self):
        self.assertEqual(
            sample._lev_jit(
                np.array(['a', 'b', 'c']),
                np.array(['a', 'a', 'a']))[-1, -1],
            2)

    def test_sample(self):
        av_l = round(
            sample.random_average_levenshtein(2, 1000, np.arange(2))[-1, -1])
        self.assertEqual(av_l, 1)


if __name__ == '__main__':
    unittest.main()
