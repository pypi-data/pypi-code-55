"""Type and size check all series"""
import jax.numpy as jnp
import pytest

from timecast.series import arma
from timecast.series import crypto
from timecast.series import enso
from timecast.series import lds
from timecast.series import lstm
from timecast.series import random
from timecast.series import rnn
from timecast.series import sp500
from timecast.series import uci
from timecast.series import unemployment


@pytest.mark.parametrize(
    "module", [arma, crypto, enso, lds, lstm, random, rnn, sp500, uci, unemployment]
)
def test_series(module):
    """Test outputs, shapes of data time series"""
    X, y = getattr(module, "generate")()  # noqa: B009

    assert isinstance(X, jnp.ndarray)
    assert isinstance(y, jnp.ndarray)
    assert X.shape[0] == y.shape[0]
