#!/usr/bin/env python

import unittest
import numpy as np
import expected_levenshtein.sample as sample
import expected_levenshtein.fit as fit


class TestFitting(unittest.TestCase):
    def test_sample(self):
        av_l = sample.random_average_levenshtein(25, 1000, np.arange(2))
        model_rows, coeffs, mses = fit.model_average_levenshtein(av_l)
        self.assertEqual(len(coeffs[0]), 6)


if __name__ == '__main__':
    unittest.main()
