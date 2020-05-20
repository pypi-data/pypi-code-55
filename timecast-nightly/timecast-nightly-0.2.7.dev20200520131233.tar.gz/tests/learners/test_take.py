"""timecast.learners.take: testing"""
import flax
import jax
import numpy as np
import pytest

from timecast.learners import Take
from timecast.utils import random

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_index(shape, index):
    """Generate Take model and state"""
    with flax.nn.stateful() as state:
        model_def = Take.partial(index=index)
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
def test_index(shape):
    """Test Take"""
    model, state = create_index(shape, index=0)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    np.testing.assert_array_almost_equal(X[0], ys)


@pytest.mark.parametrize("shape", shapes)
def test_index_bad_index(shape):
    """Test bad_index"""
    with pytest.raises(IndexError):
        _, _ = create_index(shape, index=-1)


def test_index_scalar():
    """Test scalar input"""
    model, state = create_index((2, 1), index=0)
    with pytest.raises(ValueError):
        with flax.nn.stateful(state) as state:
            _ = model(1)
