"""timecast.utils.random: testing"""
import jax.numpy as jnp

from timecast.utils import random


def test_random():
    """Test random singleton"""
    random.set_key()
    random.set_key(0)
    assert jnp.array_equal(jnp.array([0, 0]), random.get_key())
    expected = jnp.array([2718843009, 1272950319], dtype=jnp.uint32)
    assert jnp.array_equal(random.generate_key(), expected)
    expected = jnp.array([4146024105, 967050713], dtype=jnp.uint32)
    assert jnp.array_equal(random.get_key(), expected)
