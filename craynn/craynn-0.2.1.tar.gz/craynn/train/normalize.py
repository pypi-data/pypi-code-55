import tensorflow as tf

from .. import layers, parameters
from .. import updates

__all__ = [
  'normalize_weights',
  'normalize_weights_gradient',
  'get_outputs_without_activation'
]

def normalize_layer(layer : layers.Layer, substitutes, weights=True, biases=True, learning_rate=1e-1, n_iter=16):
  from ..nonlinearities import linear

  W_vars = parameters.get_variables(layer, weights=True) if weights else tuple()
  b_vars = parameters.get_variables(layer, biases=True) if biases else tuple()

  if hasattr(layer, 'activation'):
    old_activation = getattr(layer, 'activation')
    setattr(layer, 'activation', linear())
  else:
    old_activation = None

  output = layers.get_output(layer, substitutes=substitutes)

  if len(W_vars) == 0 and len(b_vars) == 0:
    if hasattr(layer, 'activation'):
      setattr(layer, 'activation', old_activation)

    return output

  for _ in range(n_iter):
    mean = tf.reduce_mean(output)
    std = tf.sqrt(tf.reduce_mean((output - mean) ** 2))

    if len(b_vars) > 0:
      offset = mean / len(b_vars)

      for var in b_vars:
        var.assign(var - learning_rate * offset)

    if len(W_vars) > 0:
      scale = tf.math.pow(std, 1 / len(W_vars))

      for var in W_vars:
        var.assign(var * tf.exp(-learning_rate * tf.math.log(scale)))

    output = layers.get_output(layer, substitutes=substitutes)

  if hasattr(layer, 'activation'):
    setattr(layer, 'activation', old_activation)

  return output

def normalize_weights(network, inputs, weights=True, biases=True, learning_rate=1e-1, n_iter=128, progress=None):
  """
  WARNING: this procedure assumes that output of each layer is sublinear with respect to its inputs, i.e.:
  `f(x, scale * W, b) <= scale * f(x, W, b)`
  and
  `f(x, W, b + offset) <= f(x, W, b) + offset`

  While this assumption is satisfied for the most of the commonly used layers, care should be taken.
  """

  cached = dict(zip(network.inputs(), inputs))

  all_layers = network.layers()

  if progress is None:
    progress = lambda x, *args, **kwargs: x

  for layer in progress(all_layers, desc='normalization'):
    cached[layer] = normalize_layer(
      layer, cached,
      weights=weights, biases=biases,
      learning_rate=learning_rate, n_iter=n_iter
    )

def get_outputs_without_activation(layers, substitutes, **modes):
  from ..layers import get_all_outputs
  from ..nonlinearities import linear

  result = list()
  cached = dict(substitutes)

  for layer in layers:
    if hasattr(layer, 'activation'):
      old_activation = getattr(layer, 'activation')
      setattr(layer, 'activation', linear())
    else:
      old_activation = None

    cached.update(
      get_all_outputs(layer, substitutes=cached, **modes)
    )
    result.append(cached[layer])

    if old_activation is not None:
      cached[layer] = old_activation(cached[layer])
      setattr(layer, 'activation', old_activation)

  return result

def normalize_weights_gradient(
  network, inputs,
  optimizer=updates.tf_updates.adam(), n_iterations=1024,
  progress=None, **properties
):
  from ..objectives import output_gaussian_normalization

  if progress is None:
    progress = lambda x, *args, **kwargs: x

  normalization = output_gaussian_normalization()

  @tf.function(autograph=False)
  def loss():
    outputs = get_outputs_without_activation([
        layer
        for layer in network.layers()
        if hasattr(layer, 'activation')
        if len(getattr(layer, 'parameter', tuple)()) > 0
      ],
      substitutes=dict(zip(network.inputs(), inputs))
    )

    return normalization(*outputs)

  opt = optimizer(loss, network.variables(**properties))

  for _ in progress(range(n_iterations), desc='normalization'):
    opt()
