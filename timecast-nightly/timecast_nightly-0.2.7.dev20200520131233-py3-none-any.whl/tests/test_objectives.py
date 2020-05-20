"""timecast.objectives: testing"""
import jax.numpy as jnp

from timecast.objectives import residual
from timecast.objectives import xboost


def model(x):
    """Dummy ensemble model"""
    return [1, 2, 3, 4, 5]


def loss_fn(true, pred):
    """Dummy loss function"""
    return jnp.square(true - pred).mean()


def test_residual():
    """Test residual objective"""
    loss, y_hat = residual(0, 10, loss_fn, model)

    assert loss == 90 and y_hat == 15


def test_xboost():
    """Test xboost objective"""
    loss, y_hat = xboost(0.0, 10.0, loss_fn, model)

    assert jnp.isclose(loss, 264.83334) and jnp.isclose(y_hat, 3.6666667)
