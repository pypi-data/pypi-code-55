from abc import abstractmethod

import tensorflow as tf

__ALL__=['BaseComponent', 'DeterministicComponent', 'StochasticComponent']


class BaseComponent(object):
    """
    The :class:`Component` is the base class for constitutional components of generative dialogue models.
    It supports batch inputs and batch outputs.
    Each component consists of a series of operations and targets a specific function.
    The components could be categorized into either deterministic or stochastic types.

    The typical input shape for :class:`Component` is like ``[batch_shape,input_shape]``,
    where ``input_shape`` represents the shape of non-batch input parameter,
    ``batch_shape`` represents how many independent inputs are fed into the :class:`Component`.

    The outputs are usually of shape ``[batch_shape, value_shape]``,
    where ``value_shape`` is the non-batch value shape of the :class:`Component`.
    Particularly, for stochastic components,
    the outputs could be of shape ``[n_sample, batch_shape, value_shape]``.
    The first additional axis is omitted only when passed n_samples is None (by default),
    in which case one sample is generated.

    The parameter dtype represents type of outputs.
    It is automatically determined from parameter types.
    And dtype must be among int16, int32, int64, float16, float32 and float64.
    When two or more parameters are tensors and they have different type, `TypeError` will be raised.

    Parameters
    ----------
    name: string
        The name of the component.
    input_shape:
        The tensor shape of inputs.
    output_shape:
        The tensor shape of outputs.
    category:
        The category of the component. either "deterministic" or "stochastic".
    dtype:
        The value type of outputs from the component.
    """
    def __init__(self, name, input_shape, output_shape, category, dtype):
        self._name = name
        self._input_shape = input_shape
        self._output_shape = output_shape
        self._dtype = dtype
        self._category = category

        if category not in ("deterministic", "stochastic"):
            raise ValueError("category can be either 'deterministic' or 'stochastic'.")

    @property
    def name(self):
        """The name of the component."""
        return self._name

    @property
    def input_shape(self):
        """The shape of the inputs into the component. A TensorShape object."""
        return self._name

    @property
    def output_shape(self):
        """The shape of the outputs from the component. A TensorShape object."""
        return self._output_shape

    @property
    def dtype(self):
        """The value type of outputs from the component."""
        return self._dtype

    @property
    def category(self):
        """The category of the component. It could be either `Stochastic` or `Deterministic`."""
        return self._category


class DeterministicComponent(BaseComponent):
    """
    The :class:`DeterministicComponent` is class for deterministic components of generative dialogue
    models.
    """
    def __init__(self, name, input_shape, output_shape, dtype):
        BaseComponent.__init__(self, name, input_shape, output_shape, "deterministic", dtype)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class StochasticComponent(BaseComponent):
    """
    The :class:`StochasticComponent` is class for stochastic components of generative dialogue
    models.
    It defines a variable distribution and supports stochastic sampling operation.

    Parameters
    ----------
    name: string
        The name of the component.
    n_samples: integer
        The number of samples to be generated.
    """
    def __init__(self, name, n_samples=None, dtype=tf.float32):
        BaseComponent.__init__(self, name, [], [], "stochastic", dtype)

        self._n_samples = n_samples
        self._distribution = None

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @property
    def n_samples(self):
        """The number of samples to be generated from the component."""
        return self._n_samples

    def sample(self, n_sample=None):
        """Sampling any number of instances from the component."""
        return self._distribution.sample(n_sample)


