import numpy as np
import tensorflow as tf

from .meta import *

__all__ = [
  'zeros_init',
  'ones_init',
  'const_init',

  'normal_init',
  'uniform_init',
]

zeros_init = as_free_parameter(tf.zeros)
ones_init = as_free_parameter(tf.ones)


def _const(shape, value, dtype=tf.float32, name=None):
  if hasattr(value, 'shape') and len(value.shape) > 0:
    assert value.shape == shape, \
      'If `value` is a non-scalar array then `shape` (%s) must be equal to `value.shape` (%s)' % (shape, value.shape)

    return tf.constant(value, dtype=dtype, name=name)
  else:
    return tf.constant(
      np.ones(shape=shape, dtype=dtype) * value,
      dtype=dtype, name=name
    )

const_init = as_free_parameter(_const)
normal_init = as_free_parameter(tf.random.normal)
uniform_init = as_free_parameter(tf.random.uniform)