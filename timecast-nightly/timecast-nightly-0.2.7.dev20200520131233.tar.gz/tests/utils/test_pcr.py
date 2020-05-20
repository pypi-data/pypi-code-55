"""timecast.utils.pcr: testing"""
import jax
import numpy as np
import pytest
from sklearn.decomposition import PCA

from timecast.utils import random
from timecast.utils.pcr import compute_projection


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (2, 10), (10, 2)])
def test_compute_projection(shape):
    """Test PCA projection of X vs X.T @ X"""
    X = jax.random.uniform(random.generate_key(), shape=shape)
    XTX = X.T @ X

    k = 1 if X.ndim == 1 else min(X.shape)
    p1 = compute_projection(X, k)
    p2 = compute_projection(XTX, k)

    np.testing.assert_array_almost_equal(abs(p1), abs(p2), decimal=3)


@pytest.mark.parametrize("shape", [(1, 1), (10, 1), (1, 10), (10, 10)])
def test_compute_projection_sklearn(shape):
    """Test PCA projection of X vs sklearn"""
    X = jax.random.uniform(random.generate_key(), shape=shape)

    projection = compute_projection(X, 1, center=True)

    pca = PCA(n_components=1)
    pca.fit(X)

    np.testing.assert_array_almost_equal(abs(projection), abs(pca.components_.T), decimal=3)
