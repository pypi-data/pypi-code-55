import pyconrad.autoinit
import os

import numpy as np


def test_conversion_1d():

    dim = 1
    random_matrix = np.random.randn(
        100).astype(pyconrad.java_float_dtype)

    grid = pyconrad.PyGrid.from_numpy(random_matrix).grid
    converted = pyconrad.PyGrid.from_grid(grid)

    assert np.allclose(converted, random_matrix)


def test_conversion():

    for dim in range(2, 5):
        random_matrix = np.random.randn(
            *[(10 * (i + 1)) for i in range(dim)])

        grid = pyconrad.PyGrid.from_numpy(random_matrix).grid
        converted = pyconrad.PyGrid.from_grid(grid)

        assert np.allclose(converted, random_matrix)
