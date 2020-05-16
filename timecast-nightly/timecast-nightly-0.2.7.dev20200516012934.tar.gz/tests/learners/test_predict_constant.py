"""timecast.learners.PredictConstant: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from timecast.learners import PredictConstant
from timecast.utils import random

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_predict_constant(shape, c):
    """Create PredictConstant model"""
    model_def = PredictConstant.partial(c=c)
    with flax.nn.stateful() as state:
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("c", [-1, 0, 1, 0.1])
def test_predict_constant_scalar(shape, c):
    """Test scalar constant"""
    model, state = create_predict_constant(shape, c)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    np.testing.assert_array_almost_equal(jnp.ones_like(X) * c, ys)


@pytest.mark.parametrize("shape", shapes)
def test_predict_constant_vector(shape):
    """Test vector constant"""
    c = jax.random.uniform(random.generate_key(), shape=shape)
    model, state = create_predict_constant(shape, c)

    X = jax.random.uniform(random.generate_key(), shape=shape)
    with flax.nn.stateful(state) as state:
        ys = model(X)

    np.testing.assert_array_almost_equal(c, ys)


@pytest.mark.parametrize("shape", shapes)
def test_predict_constant_exception(shape):
    """Test exceptional behavior"""
    shape = (dim + 1 for dim in shape)
    c = jax.random.uniform(random.generate_key(), shape=shape)
    with pytest.raises(ValueError):
        model, state = create_predict_constant(shape, c)
