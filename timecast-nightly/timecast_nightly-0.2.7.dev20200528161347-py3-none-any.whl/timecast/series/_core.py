"timecast.series._core"
import jax.numpy as jnp
import pandas as pd


def generate_timeline(path: str, name=None, delimiter=","):
    """Convenience function to grab a single time series and convert to X, y pair"""
    data = pd.read_csv(path, delimiter=delimiter)

    if name is not None:
        data = data[[name]]

    return jnp.asarray(data)[:-1].reshape(-1, 1), jnp.asarray(data)[1:].reshape(-1, 1)
