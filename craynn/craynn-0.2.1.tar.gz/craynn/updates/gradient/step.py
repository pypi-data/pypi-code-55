import tensorflow as tf

from ..reducers import momentum_average

__all__ = [
  'gradient_step',
  'momentum_step',
  'nesterov_step',
]

class GradientStep(object):
  def __init__(self, *var_spec):
    pass

  def __call__(self, grads):
    return grads

def gradient_step():
  def step(var_spec):
    return GradientStep(var_spec)

  return step

class MomentumStep(momentum_average):
  def __init__(self, var_spec, rho=0.99, initial_value=None):
    super(MomentumStep, self).__init__(*var_spec, rho=rho, initial_value=initial_value)

def momentum_step(rho=0.99):
  def step(var_spec):
    return MomentumStep(var_spec, rho=rho)

  return step

class NesterovStep(object):
  def __init__(self, var_spec, rho=0.99):
    self.momentum = momentum_average(*var_spec, rho)

  def __call__(self, grads):
    return [
      g + self.momentum.rho * m
      for g, m in zip(grads, self.momentum(grads))
    ]

def nesterov_step(rho=0.99):
  def step(var_spec):
    return NesterovStep(var_spec, rho)

  return step

