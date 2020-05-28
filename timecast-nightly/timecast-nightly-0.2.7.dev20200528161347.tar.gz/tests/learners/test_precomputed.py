"""timecast.learners.precomputed: testing"""
import flax
import jax
import numpy as np

from timecast.learners import Precomputed
from timecast.utils import random


def test_precomputed():
    """Testing Precomputed"""
    arr = jax.random.uniform(random.generate_key(), shape=(10, 10))
    with flax.nn.stateful() as state:
        model_def = Precomputed.partial(arr=arr, name="Precomputed")
        _, params = model_def.init_by_shape(random.generate_key(), [(10, 10)])
        model = flax.nn.Model(model_def, params)

    for i in range(arr.shape[0]):
        with flax.nn.stateful(state) as state:
            np.testing.assert_array_equal(arr[i], model(None))
