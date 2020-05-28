"""Objective functions for composing loss functions for multiple learners"""
import jax


def residual(x, y, loss_fn, model):
    """List of learners where each learner trains on the residual of the previous"""
    y_hats = model(x)
    target, y_hat, loss = y, y_hats[0], 0.0
    for i in range(len(y_hats) - 1):
        target -= y_hats[i]
        loss += loss_fn(target, y_hats[i + 1])
        y_hat += y_hats[i + 1]
    return loss, y_hat


def xboost(x, y, loss_fn, model):
    """List of learners governed by xboost

    Notes:
        * See: https://arxiv.org/pdf/1906.08720.pdf
    """
    y_hats = model(x)
    g = jax.grad(loss_fn)
    u, loss = 0.0, 0.0
    for i in range(len(y_hats)):
        eta = 2.0 / (i + 2.0)
        loss += g(y, u) * y_hats[i] + (1.0 / 2.0) * y_hats[i] * y_hats[i]
        u = (1.0 - eta) * u + eta * y_hats[i]
    return loss.reshape(()), u
