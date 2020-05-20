"""Linear transformation"""
from typing import Iterable

import flax
import jax
import jax.numpy as jnp


default_kernel_init = flax.nn.initializers.lecun_normal()


def _normalize_axes(axes, ndim):
    """
    A tuple by convention. len(axes_tuple) then also gives the rank efficiently.
    """
    return tuple([ax if ax >= 0 else ndim + ax for ax in axes])


class Linear(flax.nn.Module):
    """A linear transformation with flexible axes."""

    def apply(
        self,
        inputs,
        features,
        axis=-1,
        batch_dims=(),
        bias=True,
        dtype=jnp.float32,
        kernel_init=default_kernel_init,
        bias_init=flax.nn.initializers.zeros,
        precision=None,
    ):
        """Applies a linear transformation to the inputs along multiple dimensions.
    Args:
      inputs: The nd-array to be transformed.
      features: tuple with numbers of output features.
      axis: tuple with axes to apply the transformation on.
      batch_dims: tuple with batch axes.
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

        if not isinstance(features, Iterable):
            features = (features,)
        if not isinstance(axis, Iterable):
            axis = (axis,)
        if not isinstance(batch_dims, Iterable):
            batch_dims = (batch_dims,)
        features, axis, batch_dims = tuple(features), tuple(axis), tuple(batch_dims)

        if batch_dims:
            max_dim = jnp.max(batch_dims)
            if set(batch_dims) != set(range(max_dim + 1)):
                raise ValueError(
                    "batch_dims %s must be consecutive leading "
                    "dimensions starting from 0." % str(batch_dims)
                )

        ndim = inputs.ndim
        axis = _normalize_axes(axis, ndim)
        batch_dims = _normalize_axes(batch_dims, ndim)
        n_axis, n_features = len(axis), len(features)

        def kernel_init_wrap(rng, shape, dtype=jnp.float32):
            """Initializing and inducing correct shapes"""
            flat_shape = (
                jnp.prod(shape[:n_axis]),
                jnp.prod(shape[-n_features:]),
            )
            kernel = kernel_init(rng, flat_shape, dtype)
            return jnp.reshape(kernel, shape)

        kernel_shape = tuple([inputs.shape[ax] for ax in axis]) + features
        kernel = self.param("kernel", kernel_shape, kernel_init_wrap)
        kernel = jnp.asarray(kernel, dtype)

        contract_ind = tuple(range(n_axis))
        out = jax.lax.dot_general(
            inputs, kernel, ((axis, contract_ind), ((), ())), precision=precision
        )
        if bias:

            def bias_init_wrap(rng, shape, dtype=jnp.float32):
                """Initializing and inducing correct shapes"""
                flat_shape = (jnp.prod(shape[-n_features:]),)
                bias = bias_init(rng, flat_shape, dtype)
                return jnp.reshape(bias, shape)

            bias = self.param("bias", features, bias_init_wrap)
            # Reshape bias for broadcast.
            expand_dims = sorted(set(range(inputs.ndim)) - set(axis))
            for ax in expand_dims:
                bias = jnp.expand_dims(bias, ax)
            bias = jnp.asarray(bias, dtype)
            out = out + bias
        return out
