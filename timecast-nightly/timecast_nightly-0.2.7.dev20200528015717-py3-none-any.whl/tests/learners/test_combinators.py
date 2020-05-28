"""Test combinators"""
import flax
import jax
import numpy as np
import pytest

from timecast.learners import Parallel
from timecast.learners import Sequential
from timecast.utils import random

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


class Identity(flax.nn.Module):
    """Identity layer"""

    def apply(self, x: np.ndarray):
        """
        Args:
            x (np.ndarray): input data
        Returns:
            np.ndarray: result
        """
        return x


class Plus(flax.nn.Module):
    """Adds constant"""

    def apply(self, x, z):
        """
        Args:
            x (np.ndarray): input data
        Returns:
            np.ndarray: result
        """
        return x + z


@pytest.mark.parametrize("shape", shapes)
def test_parallel(shape):
    """Test Parallel combinator"""
    model_def = Parallel.partial(learners=[Identity, Identity])
    _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
    model = flax.nn.Model(model_def, params)

    X = jax.random.uniform(random.generate_key(), shape=(shape))
    ys = model(X)

    for y in ys:
        np.testing.assert_array_almost_equal(X, y)


@pytest.mark.parametrize("shape", shapes)
def test_sequential(shape):
    """Test Sequential combinator"""
    model_def = Sequential.partial(learners=[Identity, Plus.partial(z=2)])
    _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
    model = flax.nn.Model(model_def, params)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    ys = model(X)

    np.testing.assert_array_almost_equal(X + 2, ys)
