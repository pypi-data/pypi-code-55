"""timecast.series.rnn"""
from typing import Tuple

import jax
import jax.numpy as jnp
import numpy as np


def generate(
    n: int = 1000, input_dim: int = 5, output_dim: int = 1, hidden_dim: int = 64
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Description: output from a randomly initialized recurrent neural network
    """
    W_h = jnp.asarray(np.random.rand(hidden_dim, hidden_dim))
    W_x = jnp.asarray(np.random.rand(hidden_dim, input_dim))
    W_out = jnp.asarray(np.random.rand(output_dim, hidden_dim))
    b_h = jnp.zeros(hidden_dim)
    hidden = jnp.zeros(hidden_dim)

    def step(h, x):
        """Internal function for RNN step"""
        hid = jnp.tanh(jnp.dot(W_h, h) + jnp.dot(W_x, x) + b_h)
        y = jnp.dot(W_out, hid)
        return hid, y

    X = jnp.asarray(np.random.rand(n, input_dim))
    hidden, y = jax.lax.scan(step, hidden, X)

    return X, y.reshape(-1, 1)
