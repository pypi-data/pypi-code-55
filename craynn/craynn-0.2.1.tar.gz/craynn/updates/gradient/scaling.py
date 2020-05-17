import tensorflow as tf

from ..reducers import moving_sum, moving_average, max_average

__all__ = [
  'no_scaling',
  'l2_scaling',
  'total_path_scaling',
  'max_scaling'
]

class NoScaling(object):
  def __init__(self, var_spec):
    pass

  def __call__(self, grads):
    return [None for _ in grads]

def no_scaling():
  def scaling(var_spec):
    return NoScaling(var_spec)

  return scaling

class TotalPathScaling(object):
  def __init__(self, var_spec):
    self.moments = moving_sum(*var_spec)

  def __call__(self, grads):
    return [
      tf.sqrt(m)
      for m in self.moments([ g ** 2 for g in grads ])
    ]

def total_path_scaling():
  def scaling(var_spec):
    return TotalPathScaling(var_spec)

  return scaling

class L2Scaling(object):
  def __init__(self, var_spec, rho=0.99, eps=1e-7):
    self.moments = moving_average(*var_spec, rho=rho)
    self.eps = tf.constant(eps, dtype=tf.float32)

  def __call__(self, grads):
    return [
      tf.sqrt(m) + self.eps
      for m in self.moments([ g ** 2 for g in grads ])
    ]

def l2_scaling(rho=0.99, eps=1e-7):
  def scaling(var_spec, ):
    return L2Scaling(var_spec, rho=rho, eps=eps)

  return scaling


class MaxScaling(object):
  def __init__(self, var_spec, rho=0.99, eps=1e-7):
    self.moments = max_average(var_spec, rho=rho)
    self.eps = tf.constant(eps, dtype=tf.float32)

  def __call__(self, grads):
    return [
      m + self.eps
      for m in self.moments([ tf.abs(g) for g in grads ])
    ]

def max_scaling(rho=0.99, eps=1e-7):
  def scaling(var_spec, ):
    return MaxScaling(var_spec, rho=rho)

  return scaling