"""Linear transformation"""
from typing import Iterable

import flax
import jax
import jax.numpy as jnp

from timecast.learners.base import NewMixin

default_kernel_init = flax.nn.initializers.lecun_normal()


def _normalize_axes(axes, ndim):
    """
    A tuple by convention. len(axes_tuple) then also gives the rank efficiently.

    Warning:
        * This doesn't raise when some axis is greater than ndim - 1
    """
    return tuple([ax if ax >= 0 else ndim + ax for ax in axes])


class Linear(NewMixin, flax.nn.Module):
    """A linear transformation with flexible axes."""

    def apply(
        self,
        inputs,
        output_shape,
        input_axes=-1,
        batch_axes=(),
        bias=True,
        dtype=jnp.float32,
        kernel_init=default_kernel_init,
        bias_init=flax.nn.initializers.zeros,
        precision=None,
    ):
        """Applies a linear transformation to the inputs along multiple dimensions.
    Args:
      inputs: The nd-array to be transformed.
      output_shape: tuple of output shape.
      input_axes: tuple with axes to apply the transformation on.
      batch_axes: tuple with batch axes.
      bias: whether to add a bias to the output (default: True).
      dtype: the dtype of the computation (default: float32).
      kernel_init: initializer function for the weight matrix.
      bias_init: initializer function for the bias.
      precision: numerical precision of the computation see `jax.lax.Precision`
        for details.
    Returns:
      The transformed input.
    """
        inputs = jnp.asarray(inputs, dtype)

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

        if len(input_axes) == 0:
            raise IndexError("Must have at least one input dimension")

        if len(output_shape) == 0:
            raise IndexError("Must have at least one output dimension")

        if batch_axes:
            max_dim = jnp.max(batch_axes)
            if set(batch_axes) != set(range(max_dim + 1)):
                raise ValueError(
                    "batch_axes %s must be consecutive leading "
                    "dimensions starting from 0." % str(batch_axes)
                )

        if set(batch_axes) & set(input_axes):
            raise IndexError("Batch axes and input axes must not have reused axes")

        if jnp.max(batch_axes + input_axes) >= inputs.ndim:
            raise IndexError("Not enough dimensions in input for batch/input axes")

        ndim = inputs.ndim
        input_axes = _normalize_axes(input_axes, ndim)
        batch_axes = _normalize_axes(batch_axes, ndim)
        n_input_axes, n_output_axes = len(input_axes), len(output_shape)

        def kernel_init_wrap(rng, shape, dtype=jnp.float32):
            """Initializing and inducing correct shapes"""
            flat_shape = (
                jnp.prod(shape[:n_input_axes]),
                jnp.prod(shape[-n_output_axes:]),
            )
            kernel = kernel_init(rng, flat_shape, dtype)
            return jnp.reshape(kernel, shape)

        kernel_shape = tuple([inputs.shape[ax] for ax in input_axes]) + output_shape
        kernel = self.param("kernel", kernel_shape, kernel_init_wrap)
        kernel = jnp.asarray(kernel, dtype)

        contract_ind = tuple(range(n_input_axes))
        out = jax.lax.dot_general(
            inputs, kernel, ((input_axes, contract_ind), ((), ())), precision=precision
        )

        if bias:

            def bias_init_wrap(rng, shape, dtype=jnp.float32):
                """Initializing and inducing correct shapes"""
                flat_shape = (jnp.prod(shape[-n_output_axes:]),)
                bias = bias_init(rng, flat_shape, dtype)
                return jnp.reshape(bias, shape)

            bias = self.param("bias", output_shape, bias_init_wrap)
            # Reshape bias for broadcast.
            num_expand_dims = len(set(range(inputs.ndim)) - set(input_axes))
            for _ in range(num_expand_dims):
                bias = bias[None, :]
            bias = jnp.asarray(bias, dtype)
            out = out + bias

        return out
