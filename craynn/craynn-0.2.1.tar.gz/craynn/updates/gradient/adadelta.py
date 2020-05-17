import tensorflow as tf

from ..reducers import moving_average
from .meta import GradientOptimizer

__all__ = [
  'adadelta'
]

class Adadelta(GradientOptimizer):
  def __init__(self, target, variables, learning_rate=1e-3, rho=0.99, eps=1e-7):
    super(Adadelta, self).__init__(target, variables)

    self.learning_rate = tf.constant(learning_rate, dtype=tf.float32)

    self.deltas_acc = moving_average(*variables, rho=rho, initial_value=tf.ones)
    self.second_momentum = moving_average(*variables, rho=rho)

    self.eps = tf.constant(eps, dtype=tf.float32)

  def apply_gradients(self, gradients):
    scaling = self.second_momentum([g ** 2 for g in gradients])

    deltas = [
      tf.sqrt(delta / (scale + self.eps)) * grad
      for delta, scale, grad in zip(self.deltas_acc, scaling, gradients)
    ]

    self.deltas_acc([
      delta ** 2
      for delta in deltas
    ])

    for var, delta in zip(self.variables, deltas):
      var.assign_sub(self.learning_rate * delta)

def adadelta(learning_rate=1e-1, rho=0.99, eps=1e-7):
  def optimizer(target, variables):
    return Adadelta(target, variables, learning_rate=learning_rate, rho=rho, eps=eps)

  return optimizer