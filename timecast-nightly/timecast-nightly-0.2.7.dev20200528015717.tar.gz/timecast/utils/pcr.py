"""timecast.utils.pcr"""
import jax.numpy as jnp
import numpy as np


def compute_projection(X: np.ndarray, k: int, center=False) -> np.ndarray:
    """Compute PCA projection"""

    if center:
        X = X - X.mean(axis=0)
        # X /= X.shape[0] - 1

    # Compute SVD
    # X: (steps - history_len + 1, history_len * input_dim) -> (H, d)
    # U: (H, H), but because full_matrices=False, (H, d)
    # S: (min(H, d),)
    # VT: (d, d)
    U, S, VT = jnp.linalg.svd(X, full_matrices=False, compute_uv=True)

    # Get index of top K eigen values
    top_k = (-jnp.square(S)).argsort()[:k]

    # Get projection
    # projection: (d, k)
    projection = VT[top_k].T

    return projection
