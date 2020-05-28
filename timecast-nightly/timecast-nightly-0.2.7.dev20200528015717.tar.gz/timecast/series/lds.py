"""timecast.series.lds"""
from typing import Tuple

import jax
import jax.numpy as jnp
import numpy as np


def generate(
    n: int = 1000, input_dim: int = 5, output_dim: int = 1, hidden_dim: int = 5, noise: float = 1.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Description: Simulates a randomly initialized linear dynamical system
    """

    def normalize(M, k):
        """Shrinks matrix M such that largest eigenvalue has magnitude k"""
        return k * M / jnp.linalg.norm(M, ord=2)

    A = jnp.asarray(np.random.rand(hidden_dim, hidden_dim))
    B = jnp.asarray(np.random.rand(hidden_dim, input_dim))
    C = jnp.asarray(np.random.rand(output_dim, hidden_dim))
    D = jnp.asarray(np.random.rand(output_dim, input_dim))
    h = jnp.asarray(np.random.rand(hidden_dim))

    A = normalize(A, 1.0)
    B = normalize(B, 1.0)
    C = normalize(C, 1.0)
    D = normalize(D, 1.0)

    def step(h, x):
        """Internal function for LDS step"""
        x, eps_h, eps_y = x
        h = jnp.dot(A, h) + jnp.dot(B, x) + noise * eps_h
        y = jnp.dot(C, h) + jnp.dot(D, x) + noise * eps_y
        return h, y

    X = jnp.asarray(np.random.rand(n, input_dim))
    EPS_H = jnp.asarray(np.random.rand(n, hidden_dim))
    EPS_Y = jnp.asarray(np.random.rand(n, output_dim))

    _, y = jax.lax.scan(step, h, (X, EPS_H, EPS_Y))

    return X, y.reshape(-1, 1)
