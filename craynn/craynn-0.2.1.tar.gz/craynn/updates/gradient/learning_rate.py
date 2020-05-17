import tensorflow as tf

__all__ = [
  'adam_scaling'
]

def adam_scaling(beta1, beta2):
  def decay(lr, t):
    return None #lr * tf.sqrt(1 - beta2 ** t) / (1 - beta1 ** t)

  return decay

