"""timecast.learners.pcr: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from tests.learners.test_ar import _compute_kernel_bias
from timecast.learners import PCR
from timecast.utils import internalize
from timecast.utils import random
from timecast.utils.ar import historify
from timecast.utils.pcr import compute_projection


def test_pcr_fit_index_error():
    """Test PCR fit with no data"""
    with pytest.raises(IndexError):
        PCR.fit([], input_dim=1, history_len=1)


@pytest.mark.parametrize("shape", [(100, 1), (200, 5)])
@pytest.mark.parametrize("history_len", [1, 2, 5])
def test_pcr_fit(shape, history_len):
    """Test PCR fit"""
    X = jax.random.uniform(random.generate_key(), shape=shape)
    Y = jax.random.uniform(random.generate_key(), shape=(shape[0],))

    pcr, state = PCR.fit(
        [(X, Y, None)], input_dim=shape[1], history_len=history_len, normalize=False, alpha=1.0
    )

    X = internalize(X, shape[1])[0]
    Y = internalize(Y, 1)[0]

    num_histories = X.shape[0] - history_len + 1
    X = historify(X, num_histories=num_histories, history_len=history_len)
    Y = Y[-len(X) :]

    k = shape[1] * history_len

    projection = compute_projection(X, k)
    kernel, bias = _compute_kernel_bias(X @ projection, Y, alpha=1.0)
    kernel = kernel.reshape(1, k, 1)

    np.testing.assert_array_almost_equal(
        abs(kernel), abs(pcr.params["Linear"]["kernel"]), decimal=3
    )
    np.testing.assert_array_almost_equal(abs(bias), abs(pcr.params["Linear"]["bias"]), decimal=3)


def test_pcr_apply():
    """Test PCR apply shapes"""
    pcr, state = PCR.new(
        shape=(1, 1), history_len=2, projection=jnp.eye(2), loc=0, scale=1, history=jnp.ones((2, 1))
    )

    with flax.nn.stateful(state) as state:
        scalar = pcr(1)

    with flax.nn.stateful(state) as state:
        vector = pcr(jnp.ones((1,)))

    np.testing.assert_array_almost_equal(scalar, vector)


def test_pcr_fit_value_error():
    """Test number of observations"""
    X = jax.random.uniform(random.generate_key(), shape=(1, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(10, 1))

    with pytest.raises(ValueError):
        PCR.fit([(X, Y, None)], input_dim=10, history_len=1)
