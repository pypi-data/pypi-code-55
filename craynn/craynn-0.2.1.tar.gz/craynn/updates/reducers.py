import tensorflow as tf

from craynn.utils.tf_utils import make_vars

__all__ = [
  'moving_average',
  'moving_sum',
  'momentum_average',
  'max_average',
]

class accumulator(object):
  def __init__(self, *var_spec, rho=0.99, initial_value=None):
    self.rho = tf.constant(rho, dtype=tf.float32, shape=())
    self.crho = tf.constant(1 - rho, dtype=tf.float32, shape=())

    self._acc = make_vars(var_spec, initial_value=initial_value, trainable=False)

  @tf.function
  def __call__(self, values):
    if isinstance(values, (list, tuple)):
      return tuple(
        acc.assign(self.update(acc, value))
        for acc, value in zip(self._acc, values)
      )
    else:
      acc, = self._acc
      value = values

      return acc.assign(self.update(acc, value))

  def __iter__(self):
    if isinstance(self._acc, list):
      return iter(self._acc)
    else:
      return iter([self._acc])

  def update(self, acc, value):
    raise NotImplementedError

  def accumulator(self):
    return self._acc

class moving_average(accumulator):
  def update(self, acc, value):
    return self.rho * acc + self.crho * value

class momentum_average(accumulator):
  def update(self, acc, value):
    return self.rho * acc + value

class moving_sum(object):
  def __init__(self, *var_spec, initial_value=None):
    self._acc = make_vars(var_spec, initial_value=initial_value, trainable=False)

  @tf.function
  def __call__(self, values):
    if isinstance(self._acc, list):
      return [
        acc.assign_add(value)
        for acc, value in zip(self._acc, values)
      ]
    else:
      value = values
      self._acc.assign_add(value)

  def __iter__(self):
    if isinstance(self._acc, list):
      return iter(self._acc)
    else:
      return iter([self._acc])

class max_average(accumulator):
  def update(self, acc, value):
    return tf.maximum(self.rho * acc, value)