"""timecast.learners.PredictLast: testing"""
import flax
import jax
import numpy as np
import pytest

from timecast.learners import PredictLast
from timecast.utils import random

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_predict_last(shape):
    """Generate PredictLast model and state"""
    with flax.nn.stateful() as state:
        _, params = PredictLast.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(PredictLast, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
def test_predict_last(shape):
    """Test PredictLast"""
    model, state = create_predict_last(shape)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    np.testing.assert_array_almost_equal(X, ys)
