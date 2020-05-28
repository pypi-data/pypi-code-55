"""timecast.utils.statistics: testing"""
import jax
import numpy as np
import pytest

from timecast.utils import random
from timecast.utils.statistics import OnlineStatistics


@pytest.mark.parametrize("n", [2, 10, 50, 100])
@pytest.mark.parametrize("j", [1, 10, 100])
@pytest.mark.parametrize("k", [1, 10, 100])
@pytest.mark.parametrize("func", ["sum", "mean", "std", "var", "observations", "zscore"])
def test_online_sum(n, j, k, func):
    """Test online statistics"""
    stats = OnlineStatistics(dim=k)
    X = jax.random.uniform(random.generate_key(), shape=(n, j * k))

    for i in X:
        stats.update(i.reshape(j, k))

    if func == "zscore":
        np.testing.assert_array_almost_equal(
            stats.zscore(X[0, :].reshape(j, k)), (X[0, :].reshape(j, k) - stats.mean) / stats.std,
        )
    elif func != "observations":
        result = getattr(stats, func)
        np.testing.assert_array_almost_equal(
            result, getattr(X.reshape(n * j, k), func)(axis=0).reshape(1, -1), decimal=2
        )
    else:
        assert n * j == stats.observations
