"""timecast.learners._arx_history: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from timecast.learners._arx_history import _ARXHistory
from timecast.utils import random


@pytest.mark.parametrize("constrain", [True, False])
@pytest.mark.parametrize("history_len", [1, 5])
@pytest.mark.parametrize("input_dim", [1, 5])
@pytest.mark.parametrize("batch_size", [1, 5])
def test_arx_history_helper(constrain, history_len, input_dim, batch_size):
    """Test ARX helper"""
    output_shape = input_dim
    model, state = _ARXHistory.new(
        shapes=[(1, history_len, input_dim)], output_shape=output_shape, constrain=constrain,
    )

    shape = (batch_size, history_len, input_dim)
    inputs = jax.random.uniform(random.generate_key(), shape=shape)

    kernel_shape = (
        (history_len, output_shape) if constrain else (history_len, input_dim, output_shape)
    )
    kernel = jax.random.uniform(random.generate_key(), shape=kernel_shape)
    bias = jax.random.uniform(random.generate_key(), shape=(output_shape,))

    model.params["Linear"]["kernel"] = kernel
    model.params["Linear"]["bias"] = bias

    with flax.nn.stateful(state) as state:
        result = model(inputs)

    inputs_axes = (1,) if constrain else (1, 2)
    num_expand_dims = len(set(range(inputs.ndim)) - set(inputs_axes))
    for _ in range(num_expand_dims):
        bias = bias[None, :]
    expected = (
        jnp.tensordot(inputs, kernel, axes=[inputs_axes, tuple(range(len(inputs_axes)))]) + bias
    )

    np.testing.assert_array_almost_equal(expected, result)


"""
def test_arx_history_helper_inconsistent_history_shape():
    model, state = _ARXHistory.new(shapes=[(1, 5, 10)], constrain=False)
    with flax.nn.stateful(state) as state:
        with pytest.raises(ValueError):
            model(jnp.ones((10, 1, 1)))


def test_arx_history_errors():
    targets = jnp.ones((10, 4, 1))
    features = jnp.ones((10, 2, 10))

    model, state = ARXHistory.new(shapes=[targets.shape, features.shape], constrain=False)
    model, state = ARXHistory.new(shapes=[targets.shape, features.shape], constrain=True)

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(random.generate_key(), [])

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(
                random.generate_key(), [targets.shape, features.shape]
            )
            model = flax.nn.Model(model_def, params)
            model(jnp.ones((5, 2, 10)), jnp.ones((4, 4, 1)))

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(random.generate_key(), [(), features.shape])
            model = flax.nn.Model(model_def, params)
            model(targets, features)

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(random.generate_key(), [targets.shape])
            model = flax.nn.Model(model_def, params)
            model(targets, features)

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(
                random.generate_key(), [targets.shape, features.shape]
            )
            model = flax.nn.Model(model_def, params)
            model(features=features)

    with pytest.raises(ValueError):
        model_def = ARXHistory.partial(constrain=False)
        with flax.nn.stateful() as _:
            _, params = model_def.init_by_shape(
                random.generate_key(), [targets.shape, features.shape]
            )
            model = flax.nn.Model(model_def, params)
            model(targets)
"""
