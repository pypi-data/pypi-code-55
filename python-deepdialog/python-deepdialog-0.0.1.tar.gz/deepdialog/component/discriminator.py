import tensorflow as tf

from deepdialog.component.base import DeterministicComponent

__ALL__ = ['Discriminator']


class Discriminator(DeterministicComponent):
    """
    The :class:`Discriminator` class defines the component for classifying sentences.
    It is implemented through fully-connected layers.
    """
    def __init__(self, n_classes, dropout_rate, input_dim, hidden_units, name="discriminator"):
        self._n_classes = n_classes
        self._dropout_rate = dropout_rate
        self._hidden_units = hidden_units
        self._input_dim = input_dim

        self._input_shape = tf.TensorShape([None, self._input_dim])
        self._output_shape = tf.TensorShape([None, self._n_classes])
        DeterministicComponent.__init__(self, name, self._input_shape, self._output_shape, tf.float32)

    @property
    def n_classes(self):
        """The number of classes to be classified."""
        return self._n_classes

    @property
    def dropout_rate(self):
        """The dropout rate. It means how much ratio of values to be dropped at each layer."""
        return self._dropout_rate

    @property
    def input_dim(self):
        """The input dimension."""
        return self._input_dim

    @property
    def hidden_units(self):
        """The dimension of middle layer."""
        return self._hidden_units

    def _check_input_shape(self, inputs):
        """Check whether the inputs are of the right shape."""
        err_msg = "The shape of inputs should match `input_shape`."
        try:
            inputs.get_shape()[-1].assert_is_compatible_with(self._input_shape[-1])
        except ValueError:
            raise ValueError(
                err_msg + "(inputs: {} | input_shape: {})".format(inputs.get_shape(), self._input_shape))
        return inputs


    def __call__(self, inputs):

        inputs = self._check_input_shape(inputs)
        if self._hidden_units is not None:
            dis_fc1 = tf.layers.dense(
                inputs=inputs,units=self._hidden_units, activation=tf.tanh, name="discriminator_fc1")
        else:
            dis_fc1 = inputs
        if self._dropout_rate < 1.0:
            dis_fc1 = tf.nn.dropout(dis_fc1, self._dropout_rate)
        logits = tf.layers.dense(inputs=dis_fc1,
                                 units=self._n_classes, activation=None, name="discriminator_project")
        return logits


