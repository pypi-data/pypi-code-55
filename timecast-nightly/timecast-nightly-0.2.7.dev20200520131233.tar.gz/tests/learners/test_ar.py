"""timecast.learners.AR: testing"""
import flax
import jax
import jax.numpy as jnp
import numpy as np
import pytest
from sklearn.linear_model import Ridge

from timecast.learners import AR
from timecast.utils import random
from timecast.utils.ar import historify


def _compute_kernel_bias(X: np.ndarray, Y: np.ndarray, fit_intercept=True, alpha: float = 0.0):
    """Compute linear regression parameters"""
    num_samples, num_features = X.shape

    if fit_intercept:
        if num_features >= num_samples:
            X -= X.mean(axis=0)
        X = jnp.hstack((jnp.ones((X.shape[0], 1)), X))

    reg = alpha * jnp.eye(X.shape[0 if num_features >= num_samples else 1])
    if fit_intercept:
        reg = jax.ops.index_update(reg, [0, 0], 0)

    if num_features >= num_samples:
        beta = X.T @ jnp.linalg.inv(X @ X.T + reg) @ Y
    else:
        beta = jnp.linalg.inv(X.T @ X + reg) @ X.T @ Y

    if fit_intercept:
        return beta[1:], beta[0]
    else:
        return beta, [0]


shapes = [(32, 4), (4, 32), (10,), (10, 1), (1,), (1, 10), (10, 10)]


def create_ar(shape, output_dim, history_len, history=None):
    """Create AR model"""
    model_def = AR.partial(output_dim=output_dim, history_len=history_len, history=history)
    with flax.nn.stateful() as state:
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_dim", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_ys_shape(shape, output_dim, history_len):
    """Test output shape"""
    model, state = create_ar(shape, output_dim, history_len)
    with flax.nn.stateful(state) as _:
        ys = model(jax.random.uniform(random.generate_key(), shape=shape))

    assert ys.shape == (output_dim,)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_dim", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history_shape(shape, output_dim, history_len):
    """Test history shape"""
    model, state = create_ar(shape, output_dim, history_len)
    with flax.nn.stateful(state) as state:
        _ = model(jax.random.uniform(random.generate_key(), shape=shape))

    input_features = shape[0] if len(shape) == 1 else shape[1]
    assert state.as_dict()["/"]["history"].shape == (history_len, input_features)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_dim", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history(shape, output_dim, history_len):
    """Test history values"""
    input_features = shape[0] if len(shape) == 1 else shape[1]
    history = jax.random.uniform(random.generate_key(), shape=(history_len, input_features))
    model, state = create_ar(shape, output_dim, history_len, history)

    np.testing.assert_array_almost_equal(history, state.as_dict()["/"]["history"])


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("fit_intercept", [True, False])
@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
def test_compute_kernel_bias(shape, fit_intercept, alpha):
    """Test kernel and bias computation"""
    if len(shape) == 1:
        shape += (1,)
    X = jax.random.uniform(random.generate_key(), shape=shape)
    Y = jax.random.uniform(random.generate_key(), shape=(shape[0],))

    if shape[0] > shape[1]:
        ridge = Ridge(alpha=alpha, fit_intercept=fit_intercept)
        expected = ridge.fit(X, Y)
        kernel, bias = _compute_kernel_bias(X, Y, alpha=alpha, fit_intercept=fit_intercept)
        np.testing.assert_array_almost_equal(expected.coef_, kernel, decimal=2)
        np.testing.assert_array_almost_equal(expected.intercept_, bias, decimal=2)
    else:
        # TODO: Ignore underdetermined systems for now
        _, _ = _compute_kernel_bias(X, Y, alpha=alpha, fit_intercept=fit_intercept)
        assert True


@pytest.mark.parametrize("shape", [(40, 1), (50, 2)])
@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("history_len", [1, 5, 10])
def test_ar_fit(shape, history_len, alpha):
    """Test AR class method fit"""
    X = jax.random.uniform(random.generate_key(), shape=shape)
    Y = jax.random.uniform(random.generate_key(), shape=(shape[0],))

    num_histories = shape[0] - history_len + 1
    history = historify(X, history_len, num_histories)

    kernel, bias = _compute_kernel_bias(history, Y[history_len - 1 :], alpha=alpha)
    kernel = kernel.reshape(1, history_len * shape[1], 1)
    bias = jnp.expand_dims(jnp.asarray(bias), 0)

    ar, state = AR.fit(
        [(X, Y, None)], input_dim=X.shape[1], history_len=history_len, alpha=alpha, normalize=False
    )
    ar_kernel = ar.params["Linear"]["kernel"]
    ar_bias = ar.params["Linear"]["bias"]

    np.testing.assert_array_almost_equal(kernel, ar_kernel, decimal=3)
    np.testing.assert_array_almost_equal(bias, ar_bias, decimal=3)


def test_ar_fit_value_error():
    """Test number of observations"""
    X = jax.random.uniform(random.generate_key(), shape=(1, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(10, 1))

    with pytest.raises(ValueError):
        AR.fit([(X, Y, None)], input_dim=10, history_len=1)


def test_ar_fit_index_error():
    """Test index error"""
    with pytest.raises(IndexError):
        AR.fit([], input_dim=1, history_len=10)


@pytest.mark.parametrize(
    "shape", [(1,), (1, 1), (10,), (10, 1), (1, 10), (10, 10), (20, 5), (5, 20)]
)
@pytest.mark.parametrize("history_len", [1, 5, 10])
@pytest.mark.parametrize("loc", [True, False])
@pytest.mark.parametrize("scale", [True, False])
def test_ar_apply(shape, history_len, loc, scale):
    """Test apply"""
    x = jax.random.uniform(random.generate_key(), shape=shape)
    if x.ndim == 1:
        x = x.reshape(1, -1)
    history = jax.random.uniform(random.generate_key(), shape=(history_len, x.shape[1]))
    kernel = jax.random.uniform(random.generate_key(), shape=(1, history_len * x.shape[1], 1))
    bias = jax.random.uniform(random.generate_key(), shape=(1,))

    loc = (
        jax.random.uniform(random.generate_key(), shape=(1, history_len * x.shape[1]))
        if loc
        else None
    )
    scale = (
        jax.random.uniform(random.generate_key(), shape=(1, history_len * x.shape[1]))
        if scale
        else None
    )

    with flax.nn.stateful() as _:
        model_def = AR.partial(
            history_len=history_len, history=history, loc=loc, scale=scale, name="AR"
        )
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
        model.params["Linear"]["kernel"] = kernel
        model.params["Linear"]["bias"] = bias

        result = model(x)

    expected_history = jnp.vstack((history, x))[x.shape[0] :].ravel()
    if loc is not None:
        expected_history -= loc
    if scale is not None:
        expected_history /= scale

    expected = jnp.tensordot(expected_history.reshape(1, -1), kernel) + bias

    np.testing.assert_array_almost_equal(result, expected)


def test_ar_scalar():
    """Test scalar values"""
    ar, state = AR.new((1, 1), history_len=1)
    with flax.nn.stateful(state) as state:
        assert 0 == ar(1)
