"""Helper functions and classes for timecast.learners"""
import abc
import inspect
from typing import Any
from typing import Iterable
from typing import List
from typing import Tuple

import flax
import jax.numpy as jnp
import numpy as np

from timecast.utils import random


class FitMixin(abc.ABC):
    """Mixin class that provides a fit function for offline training / learner
    initialization"""

    @classmethod
    @abc.abstractmethod
    def fit(
        cls,
        data: Iterable[Tuple[np.ndarray, np.ndarray, Any]],
        input_dim: int,
        output_dim: int = 1,
        key: jnp.ndarray = None,
        **kwargs
    ) -> flax.nn.Model:
        """Fit and initialize learner on training data

        Notes:
            * We could infer input_dim from data, but for now, require
            users to explicitly provide
            * output_dim defaults to 1 and is ignored for now

        Todo:
            * Really intended for passing in timeseries at a time, not
            individual time series observations; is this the right general API?
            * Shape is (1, input_dim); what about mini-batches?

        Args:
            data: an iterable of tuples containing input/truth pairs of time
            series plus any auxiliary value
            input_dim: number of feature dimensions in input
            output_dim: number of feature dimensions in output
            key: random key for jax random
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        raise NotImplementedError()


class NewMixin:
    """Mixin class that provides a flax.nn.Model constructor function"""

    # TODO (flax)
    @classmethod
    def new(
        cls, shapes: List[Tuple[int, ...]], *, key: jnp.ndarray = None, name: str = None, **kwargs
    ) -> flax.nn.Model:
        """
        Args:
            shapes (List[Tuple[int, ...]]): shapes for initialization
            key (jnp.ndarray): key for jax random
            name (str): identifier for top-level module
            **kwargs: arguments for flax.nn.Module
        """
        argspec = inspect.getfullargspec(cls.apply)

        num_kwargs = 0 if argspec.defaults is None else len(argspec.defaults)

        _kwargs = {}

        # Capture kwarg defaults
        for i in range(1, num_kwargs + 1):
            _kwargs[argspec.args[-i]] = argspec.defaults[-i]

        # Override kwarg defaults, if any
        for kw, arg in kwargs.items():
            if kw in argspec.args or argspec.varkw is not None:
                _kwargs[kw] = arg
            else:
                raise ValueError("Found extra kwarg {}: {}".format(kw, arg))

        model_def = cls.partial(**kwargs)

        if name is None:
            name = cls.__name__.lower()

        if key is None:
            key = random.generate_key()

        with flax.nn.stateful() as state:
            _, params = model_def.init_by_shape(key, shapes)
        model = flax.nn.Model(model_def, params)

        return model, state
