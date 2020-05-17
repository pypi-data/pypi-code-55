import tensorflow as tf

from .step import *
from .scaling import *
from .meta import GradientOptimizer

__all__ = [
  'sgd', 'momentum', 'nesterov',
  'rmsprop', 'maxprop',
  'adagrad'
]

class GenericGradientOptimizer(GradientOptimizer):
  def __init__(self, target, variables, step, scaling, learning_rate=1e-3):
    super(GenericGradientOptimizer, self).__init__(target, variables)

    self._step_op = step(variables)
    self._scaling_op = scaling(variables)

    self.learning_rate = tf.constant(learning_rate, dtype=tf.float32)

  def apply_gradients(self, gradients):
    step = self._step_op(gradients)
    scaling = self._scaling_op(gradients)

    for var, delta, scale in zip(self.variables, step, scaling):
      if scale is None:
        var.assign_sub(self.learning_rate * delta)
      else:
        var.assign_sub(self.learning_rate * delta / scale)


class SGD(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3):
    super(SGD, self).__init__(
      target, variables,
      step=gradient_step(),
      scaling=no_scaling(),
      learning_rate=learning_rate
    )

def sgd(learning_rate=1e-3):
  def optimizer(target, variables):
    return SGD(target, variables, learning_rate=learning_rate)

  return optimizer


class Momentum(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3, rho=0.99):
    super(Momentum, self).__init__(
      target, variables,
      step=momentum_step(rho),
      scaling=no_scaling(),
      learning_rate=learning_rate
    )

def momentum(learning_rate=1e-3, rho=0.99):
  def optimizer(target, variables):
    return Momentum(target, variables, learning_rate=learning_rate, rho=rho)

  return optimizer


class Nesterov(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3, rho=0.99):
    super(Nesterov, self).__init__(
      target, variables,
      step=nesterov_step(rho),
      scaling=no_scaling(),
      learning_rate=learning_rate
    )

def nesterov(learning_rate=1e-3, rho=0.99):
  def optimizer(target, variables):
    return Nesterov(target, variables, learning_rate=learning_rate, rho=rho)

  return optimizer

class RMSProp(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3, rho=0.99, eps=1e-7):
    super(RMSProp, self).__init__(
      target, variables,
      step=gradient_step(),
      scaling=l2_scaling(rho, eps),
      learning_rate=learning_rate,
    )

def rmsprop(learning_rate=1e-3, rho=0.99, eps=1e-7):
  def optimizer(target, variables):
    return RMSProp(target, variables, learning_rate=learning_rate, rho=rho, eps=eps)

  return optimizer

class MaxProp(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3, rho=0.99):
    super(MaxProp, self).__init__(
      target, variables,
      step=gradient_step(),
      scaling=max_scaling(rho),
      learning_rate=learning_rate
    )

def maxprop(learning_rate=1e-3, rho=0.99):
  def optimizer(target, variables):
    return MaxProp(target, variables, learning_rate=learning_rate, rho=rho)

  return optimizer

class Adagrad(GenericGradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-2):
    super(Adagrad, self).__init__(
      target, variables,
      step=gradient_step(),
      scaling=total_path_scaling(),
      learning_rate=learning_rate
    )

def adagrad(learning_rate=1e-3):
  def optimizer(target, variables):
    return Adagrad(target, variables, learning_rate=learning_rate)

  return optimizer