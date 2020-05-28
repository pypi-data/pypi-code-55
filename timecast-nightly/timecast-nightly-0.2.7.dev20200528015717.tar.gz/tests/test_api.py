"""timecacst.api: testing"""
import jax
import numpy as np

from timecast.api import tscan
from timecast.learners import AR
from timecast.learners import PredictLast
from timecast.optim import DummyGrad
from timecast.utils import random


def test_tscan_no_objective():
    """Test tscan without objective"""
    optimizer_def = DummyGrad(add=4.0)
    model, state = PredictLast.new([(1, 10)])
    optimizer = optimizer_def.create(model)

    X = jax.random.uniform(random.generate_key(), shape=(5, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(5, 10))
    pred, optimizer, state = tscan(X, Y, optimizer)

    np.testing.assert_array_equal(X, pred)

    # TODO (flax): this will fail once we remove dummy
    assert 20 == optimizer.target.params["dummy"]


def test_tscan_state():
    """Test tscan with stateful learner"""
    optimizer_def = DummyGrad(add=4.0)
    model, state = AR.new([(1, 10)], output_dim=1, history_len=1)
    optimizer = optimizer_def.create(model)

    X = jax.random.uniform(random.generate_key(), shape=(5, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(5, 10))
    pred, optimizer, state = tscan(X, Y, optimizer, state=state)

    np.testing.assert_array_equal(state.state["/"]["history"], X[-1, :].reshape(1, -1))
    np.testing.assert_array_equal(optimizer.target.params["Linear"]["bias"], 20.0)
