"""timecast.learners._learner: testing"""
from typing import Iterable

import flax
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from timecast.learners import Linear
from timecast.learners._linear import _normalize_axes
from timecast.utils import random


def get_kernel_bias(model):
    """Utility function to get kernel and bias params"""
    return model.params["kernel"], model.params["bias"]


def eval_model(model, state, inputs):
    """Utility function to evaluate a model with inputs"""
    with flax.nn.stateful(state) as state:
        result = model(inputs)
    return result


@pytest.mark.parametrize(
    "axes,ndim,expected", [((0, 1), 3, (0, 1)), ((-1, 0), 3, (2, 0)), ((4, 0), 3, (4, 0))]
)
def test_normalize_axes(axes, ndim, expected):
    """Test utility function for normalizing axes"""
    assert _normalize_axes(axes, ndim) == expected


@pytest.mark.parametrize("output_shape", [(), 1, (1,), (1, 2), (2, 1), (2, 2), (3, 2, 4)])
@pytest.mark.parametrize("input_axes", [(), -1, 1, (1,), (1, 2), (2, 3)])
@pytest.mark.parametrize("batch_axes", [(), 1, (1,), 0, (0,), (0, 1)])
def test_linear(output_shape, input_axes, batch_axes):
    """Test linear

    Todo:
        * Separate tests for exceptional behavior to get rid of duplicate tests
        and sloppy code
    """
    orig_output_shape, orig_input_axes, orig_batch_axes = output_shape, input_axes, batch_axes

    if not isinstance(output_shape, Iterable):
        output_shape = (output_shape,)
    if not isinstance(input_axes, Iterable):
        input_axes = (input_axes,)
    if not isinstance(batch_axes, Iterable):
        batch_axes = (batch_axes,)
    output_shape, input_axes, batch_axes = (
        tuple(output_shape),
        tuple(input_axes),
        tuple(batch_axes),
    )

    shapes = [
        tuple(jax.random.randint(random.get_key(), (len(batch_axes) + len(input_axes),), 0, 100))
    ]

    if len(input_axes) == 0 or len(output_shape) == 0:
        with pytest.raises(IndexError):
            Linear.new(
                shapes=shapes,
                output_shape=output_shape,
                input_axes=input_axes,
                batch_axes=batch_axes,
            )

    elif batch_axes and set(batch_axes) != set(range(jnp.max(batch_axes) + 1)):
        with pytest.raises(ValueError):
            Linear.new(
                shapes=shapes,
                output_shape=output_shape,
                input_axes=input_axes,
                batch_axes=batch_axes,
            )

    elif set(batch_axes) & set(input_axes):
        with pytest.raises(IndexError):
            Linear.new(
                shapes=shapes,
                output_shape=output_shape,
                input_axes=input_axes,
                batch_axes=batch_axes,
            )

    elif jnp.max(batch_axes + input_axes) >= len(shapes[0]):
        with pytest.raises(IndexError):
            Linear.new(
                shapes=shapes,
                output_shape=output_shape,
                input_axes=input_axes,
                batch_axes=batch_axes,
            )
    else:
        model, state = Linear.new(
            shapes=shapes,
            output_shape=orig_output_shape,
            input_axes=orig_input_axes,
            batch_axes=orig_batch_axes,
        )

        inputs = jax.random.uniform(random.generate_key(), shape=shapes[0])
        ndim = inputs.ndim

        input_axes = _normalize_axes(input_axes, ndim)
        batch_axes = _normalize_axes(batch_axes, ndim)

        kernel, bias = get_kernel_bias(model)
        result = eval_model(model, state, inputs)

        expected = (
            jnp.tensordot(
                inputs, kernel, axes=(input_axes, tuple(range(kernel.ndim - len(output_shape))))
            )
            + bias
        )

        np.testing.assert_array_almost_equal(expected, result)
