import tensorflow as tf
import numpy as np

__all__ = ['gelu', 'gelu_layer', 'gelu_new', 'gelu_new_layer', 'swish', 'swish_layer']


# >>> Code below import from huggingface transformer >>>
def gelu(x):
    """ Gaussian Error Linear Unit.
    Original Implementation of the gelu activation function in Google Bert repo when initially created.
        For information: OpenAI GPT's gelu is slightly different (and gives slightly different results):
        0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))
        Also see https://arxiv.org/abs/1606.08415
    """
    cdf = 0.5 * (1.0 + tf.math.erf(x / tf.math.sqrt(2.0)))
    return x * cdf


def gelu_new(x):
    """Gaussian Error Linear Unit.
    This is a smoother version of the RELU.
    Original paper: https://arxiv.org/abs/1606.08415
    Args:
        x: float Tensor to perform activation.
    Returns:
        `x` with the GELU activation applied.
    """
    cdf = 0.5 * (1.0 + tf.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf


def swish(x):
    return x * tf.sigmoid(x)


ACT2FN = {
    "gelu":     tf.keras.layers.Activation(gelu),
    "relu":     tf.keras.activations.relu,
    "swish":    tf.keras.layers.Activation(swish),
    "gelu_new": tf.keras.layers.Activation(gelu_new),
}
# <<< END <<<
# Visit https://github.com/huggingface/transformers for more information
gelu_layer = tf.keras.layers.Activation(gelu)
relu_layer = tf.keras.activations.relu
swish_layer = tf.keras.layers.Activation(swish)
gelu_new_layer = tf.keras.layers.Activation(gelu_new)
