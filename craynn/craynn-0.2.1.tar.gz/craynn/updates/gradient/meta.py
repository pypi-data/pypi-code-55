import tensorflow as tf

__all__ = [
  'GradientOptimizer',
  'OptimizerModel',
  'optimizer_model_from'
]

class GradientOptimizer(object):
  def __init__(self, target, variables):
    self.target = target
    self.variables = variables

    self.tape = None

  def __enter__(self):
    if self.tape is not None:
      raise RuntimeError('Reentering optimizer context')

    self.tape = tf.GradientTape(persistent=False, watch_accessed_variables=False)
    self.tape.__enter__()
    self.tape.watch(self.variables)

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.tape.__exit__(exc_type, exc_val, exc_tb)
    self.tape = None

  def apply_gradients(self, gradients):
    raise NotImplementedError()

  def step(self, *args):
    if self.tape is None:
      raise RuntimeError('step is called without entering optimizer context, please, consider using __call__ instead')

    value = self.target(*args)

    if isinstance(value, (tuple, list)):
      value_ = sum(value)
    else:
      value_ = value

    gradients = self.tape.gradient(value_, self.variables)
    self.apply_gradients(gradients)

    return value

  @tf.function
  def __call__(self, *args):
    with self:
      return self.step(*args)

class OptimizerModel(object):
  pass

def optimizer_model_from(clazz):
  from craygraph import CarringExpression
  return CarringExpression(
    clazz, carried=('target', 'variables'),
    base_constructor_class=OptimizerModel
  )