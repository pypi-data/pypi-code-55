from data_cache import numpy_cache, pandas_cache

from datetime import datetime
import numpy as np
import pandas as pd


@numpy_cache("a", "c")
def simple_func(a, *args, **kwargs):
    return np.array([[1, 2, 3], [2, 3, 4]]), np.array([[1, 2, 3], [2, 3, 4]]) * 10


@numpy_cache("a", "c")
def simple_func2(a, *args, **kwargs):
    return np.array([[1, 2, 3], [2, 3, 4]])


@pandas_cache("a", "c")
def simple_func3(a, *args, **kwargs):
    return pd.DataFrame([[1, 2, 3], [2, 3, 4]]), pd.DataFrame([[1, 2, 3], [2, 3, 4]]) * 10


@pandas_cache("a", "c")
def simple_func4(a, *args, **kwargs):
    return pd.DataFrame([[1, 2, 3], [2, 3, 4]])


simple_func(1, c=2)
simple_func(2, c=2)
simple_func(3, c=2)
simple_func2(2, c=2)
simple_func2(3, c=2)
simple_func3(3, c=2)
simple_func4(3, c=2)
