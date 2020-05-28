"""timecast.utils.ar: testing"""
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from tests.learners.test_ar import _compute_kernel_bias
from timecast.utils import random
from timecast.utils.ar import _compute_xtx_inverse
from timecast.utils.ar import _fit_constrained
from timecast.utils.ar import _fit_unconstrained
from timecast.utils.ar import _form_constraints
from timecast.utils.ar import compute_gram
from timecast.utils.ar import fit_gram
from timecast.utils.ar import historify
from timecast.utils.gram import OnlineGram


@pytest.mark.parametrize("m", [1, 10])
@pytest.mark.parametrize("n", [1, 10])
@pytest.mark.parametrize("history_len", [-1, 0, 1, 10])
@pytest.mark.parametrize("num_histories", [0, 1, 10])
@pytest.mark.parametrize("offset", [0, 1, 10])
def test_historify(m, n, history_len, num_histories, offset):
    """Test history-making"""
    X = jax.random.uniform(random.generate_key(), shape=(m, n))

    if (
        num_histories < 1
        or history_len < 1
        or X.shape[0] < offset + num_histories + history_len - 1
    ):
        with pytest.raises(ValueError):
            historify(X, num_histories, history_len, offset)

    else:
        batched = historify(X, history_len, num_histories, offset)

        for i, batch in enumerate(batched):
            np.testing.assert_array_almost_equal(
                X[i + offset : i + offset + history_len].reshape(-1), batch
            )


@pytest.mark.parametrize("n", [100])
@pytest.mark.parametrize("input_dim", [1, 5])
@pytest.mark.parametrize("output_dim", [1, 4])
@pytest.mark.parametrize("history_len", [1, 3])
def test_compute_gram(n, input_dim, output_dim, history_len):
    """Test compouting gram matrices"""
    X = jax.random.uniform(random.generate_key(), shape=(n, input_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, output_dim))

    XTX, XTY = compute_gram([(X, Y, None)], input_dim, output_dim, history_len)

    history = historify(X, history_len, n - history_len + 1)
    np.testing.assert_array_almost_equal(history.T @ history, XTX.matrix(), decimal=4)
    np.testing.assert_array_almost_equal(history.T @ Y[history_len - 1 :], XTY.matrix(), decimal=4)


def test_compute_gram_no_data():
    """Test no data"""
    with pytest.raises(ValueError):
        compute_gram([(jnp.zeros((0, 1)), jnp.zeros((0, 1)), None)], 1, 1, 1)

    with pytest.raises(IndexError):
        compute_gram([], 1, 1, 1)


def test_compute_gram_underdetermined():
    """Test underdetermined"""
    data = jnp.ones((13, 10))
    with pytest.raises(ValueError):
        compute_gram([(data, data, None)], 10, 10, 10)


def test_fit_gram_underdetermined():
    """Test underdetermined"""
    XTX = OnlineGram(1)
    XTY = XTX

    with pytest.raises(ValueError):
        fit_gram(XTX, XTY)


@pytest.mark.parametrize(
    "history_len,input_dim,output_dim,fit_intercept,expected_R,expected_r",
    [
        (
            3,
            2,
            1,
            False,
            np.array(
                [
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0],
                ]
            ),
            np.zeros(3),
        ),
        (
            3,
            2,
            1,
            True,
            np.array(
                [
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -1.0],
                ]
            ),
            np.zeros(4),
        ),
        (4, 1, 1, True, np.zeros((0, 5)), np.zeros((0))),
        (
            3,
            2,
            2,
            True,
            np.array(
                [
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -1.0],
                ]
            ),
            np.zeros((4, 2)),
        ),
    ],
)
def test_form_constraints(
    history_len, input_dim, output_dim, fit_intercept, expected_R, expected_r
):
    """Test forming constraints"""
    R, r = _form_constraints(input_dim, output_dim, history_len, fit_intercept)

    r = r.squeeze()

    assert np.array_equal(expected_R, R)
    assert np.array_equal(expected_r, r)


@pytest.mark.parametrize("n", [40, 1000])
@pytest.mark.parametrize("input_dim", [1, 5])
@pytest.mark.parametrize("output_dim", [1, 4])
@pytest.mark.parametrize("history_len", [1, 3])
def test_fit_unconstrained(n, input_dim, output_dim, history_len):
    """Fit unconstrained regression"""
    # NOTE: we use random data because we want to test dimensions and
    # correctness vs a second implementation
    X = jax.random.uniform(random.generate_key(), shape=(n, input_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, output_dim))

    XTX, XTY = compute_gram([(X, Y, None)], input_dim, output_dim, history_len)

    kernel, bias = fit_gram(XTX, XTY)
    num_histories = n - history_len + 1
    history = historify(X, history_len, num_histories)

    expected_kernel, expected_bias = _compute_kernel_bias(history, Y[history_len - 1 :], alpha=1.0)
    expected_kernel = expected_kernel.reshape(1, history_len * input_dim, -1)

    np.testing.assert_array_almost_equal(expected_kernel, kernel, decimal=3)
    np.testing.assert_array_almost_equal(expected_bias, bias, decimal=3)


@pytest.mark.parametrize("n", [1000])
@pytest.mark.parametrize("input_dim", [10, 12])
@pytest.mark.parametrize("output_dim", [1, 10])
@pytest.mark.parametrize("history_len", [2])
def test_fit_constrained(n, input_dim, output_dim, history_len):
    """Fit constrained regression"""
    # NOTE: we use random data because we want to test dimensions and
    # correctness vs a second implementation
    X = jax.random.uniform(random.generate_key(), shape=(n, input_dim))
    Y = jax.random.uniform(random.generate_key(), shape=(n, output_dim))

    XTX, XTY = compute_gram([(X, Y, None)], input_dim, output_dim, history_len)
    result = fit_gram(XTX, XTY, input_dim=input_dim)

    # Next, check that each chunk of input_dim features have the same coefficient
    # result = fit_gram(XTX, XTY, input_dim=input_dim)
    R, r = _form_constraints(
        input_dim=input_dim, output_dim=output_dim, history_len=history_len, fit_intercept=True,
    )

    XTX = XTX.matrix(fit_intercept=True, input_dim=input_dim)
    XTY = XTY.matrix(fit_intercept=True, input_dim=input_dim)
    inv = _compute_xtx_inverse(XTX, alpha=1.0)
    beta = _fit_unconstrained(inv, XTY)
    beta = _fit_constrained(beta, inv, R, r)
    beta = beta.reshape(history_len + 1, input_dim, -1)
    assert np.sum([np.abs(x - x[0]) for x in beta]) < 1e-4

    # Finally, check that resulting vector is of the correct length and the
    # values are self-consistent
    assert len(beta) == history_len + 1

    beta = beta[:, 0]
    beta = beta[1:], beta[0]

    # Check final results
    np.testing.assert_array_almost_equal(beta[0], result[0])
    np.testing.assert_array_almost_equal(beta[1], result[1])


def test_fit_constrained_bad_input_dim():
    """Bad input for constrained"""
    XTX = OnlineGram(10)
    XTY = OnlineGram(5)

    XTX.update(jax.random.uniform(random.generate_key(), shape=(100, 10)))
    XTY.update(jax.random.uniform(random.generate_key(), shape=(100, 5)))

    with pytest.raises(ValueError):
        fit_gram(XTX, XTY, input_dim=7)
