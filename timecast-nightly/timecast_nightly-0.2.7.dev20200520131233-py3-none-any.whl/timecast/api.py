"""timecast top-level API"""
from functools import partial
from typing import Callable
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as np


def _objective(x, y, loss_fn, model):
    """Default objective function"""
    y_hat = model(x)
    return loss_fn(y, y_hat), y_hat


def tscan(
    X: Union[np.ndarray, Tuple[np.ndarray, ...]],
    Y: Union[np.ndarray, Tuple[np.ndarray, ...]],
    optimizer: flax.optim.base.Optimizer,
    loss_fn: Callable[[np.ndarray, np.ndarray], np.ndarray] = lambda true, pred: jnp.square(
        true - pred
    ).mean(),
    state: flax.nn.base.Collection = None,
    objective: Callable[
        [
            np.ndarray,
            np.ndarray,
            Callable[[np.ndarray, np.ndarray], np.ndarray],
            flax.nn.base.Model,
        ],
        Tuple[np.ndarray, np.ndarray],
    ] = None,
):
    """Take gradients steps performantly on one data item at a time

    Args:
        X: np.ndarray or tuple of np.ndarray of inputs
        Y: np.ndarray or tuple of np.ndarray of outputs
        optimizer: initialized optimizer
        loss_fn: loss function to compose where first arg is true value and
        second is pred
        state: state required by flax
        objective: function composing loss functions

    Returns:
        np.ndarray: result
    """
    state = state or flax.nn.Collection()
    objective = objective or _objective

    def _tscan(optstate, xy):
        """Helper function"""
        x, y = xy
        optimizer, state = optstate
        func = partial(objective, x, y, loss_fn)
        with flax.nn.stateful(state) as state:
            (loss, y_hat), grad = jax.value_and_grad(func, has_aux=True)(optimizer.target)
        return (optimizer.apply_gradient(grad), state), y_hat

    (optimizer, state), pred = jax.lax.scan(_tscan, (optimizer, state), (X, Y))
    return pred, optimizer, state
