"""timecast.series.lstm"""
from typing import Tuple

import jax
import jax.numpy as jnp
import numpy as np


def generate(
    n: int = 1000, input_dim: int = 5, output_dim: int = 1, hidden_dim: int = 64
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Description: output from a randomly initialized LSTM
    """
    W_hh = jnp.asarray(np.random.rand(4 * hidden_dim, hidden_dim))
    W_xh = jnp.asarray(np.random.rand(4 * hidden_dim, input_dim))
    b_h = np.zeros(4 * hidden_dim)
    b_h[hidden_dim : 2 * hidden_dim] = np.ones(hidden_dim)
    b_h = jnp.asarray(b_h)
    W_out = jnp.asarray(np.random.rand(output_dim, hidden_dim))
    cell = jnp.zeros(hidden_dim)
    hidden = jnp.zeros(hidden_dim)

    def sigmoid(x):
        """Sigmoid function"""
        return 1.0 / (1.0 + jnp.exp(-x))

    def step(hc, x):
        """Internal function for LSTM step"""
        h, c = hc
        gate = jnp.dot(W_hh, h) + jnp.dot(W_xh, x) + b_h
        i, f, g, o = np.split(gate, 4)
        nc = sigmoid(f) * c + sigmoid(i) * jnp.tanh(g)
        nh = sigmoid(o) * jnp.tanh(nc)
        y = jnp.dot(W_out, nh)
        return (nh, nc), y

    X = jnp.asarray(np.random.rand(n, input_dim))
    _, y = jax.lax.scan(step, (hidden, cell), X)

    return X, y.reshape(-1, 1)
