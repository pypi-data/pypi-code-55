import tensorflow as tf
from deepdialog.utils import rnn_builder

from deepdialog.component.base import DeterministicComponent

__ALL__ = ['Encoder', "ContextEncoder"]


class Encoder(DeterministicComponent):
    """
    The :class:`Encoder` class is the encoder component of generative dialogue models,
    which encodes input sentences into real-valued vectors.
    The real-valued vectors are usually considered the summary of sentences.
    The :class:`Encoder` class is implemented through a recurrent neural network.

    The typical shape of inputs is like ``[batch_size, seq_len, embed_size]``.
    The shape of output vectors is like ``[batch_size, hidden_dim]``.
    """
    def __init__(self, embedding, params, input_keep_prob, name="vanilla_encoder"):

        self._input_shape = tf.TensorShape([None, params.seq_len])
        self._output_shape = tf.TensorShape([None, params.hidden_dim])
        self._embedding = embedding
        self._params = params
        self._input_keep_prob = input_keep_prob

        DeterministicComponent.__init__(self, name, self._input_shape, self._output_shape, tf.float32)


    def __call__(self, encoder_inputs, encoder_lengths):

        if len(encoder_inputs.get_shape()) >= 3 and \
                (len(encoder_lengths.get_shape()) + 1 == len(encoder_inputs.get_shape())):
            encoder_inputs = tf.reshape(encoder_inputs, [-1, tf.shape(encoder_inputs)[-1]])
            encoder_lengths = tf.reshape(encoder_lengths, [-1])

        with tf.variable_scope("encoder") as scope:
            encoder_embedded_inputs = tf.nn.embedding_lookup(self._embedding, encoder_inputs)
            # [batch_size, seq_len, embed_size]

        if self._params.encoder_type == "uni":
            encoder_cell = rnn_builder.create_rnn_cell(
                self._params.cell_type, self._params.hidden_dim, self._params.num_layers,
                use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

            encoder_outputs, encoder_states = tf.nn.dynamic_rnn(
                cell=encoder_cell, inputs=encoder_embedded_inputs,
                sequence_length=encoder_lengths, dtype=tf.float32,
                swap_memory=True)

            # gru: [batch_size, seq_len, hidden_size] [batch_size, hidden_size]
            # lstm: [batch_size, hidden_size] * num_layers
            return encoder_outputs, encoder_states

        elif self._params.encoder_type == "bi":

            fw_cell = rnn_builder.create_rnn_cell(
                self._params.cell_type, self._params.hidden_units, self._params.num_layers,
                use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

            bw_cell = rnn_builder.create_rnn_cell(
                self._params.cell_type, self._params.hidden_units, self._params.num_layers,
                use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

            encoder_outputs, encoder_states = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=fw_cell, cell_bw=bw_cell, inputs=encoder_embedded_inputs,
                dtype=tf.float32, sequence_length=encoder_lengths, swap_memory=True)
            return encoder_outputs, encoder_states

        else:
            raise ValueError("Unknown encoder_type Error: %s" % self._params.encoder_type)



class ContextEncoder(DeterministicComponent):
    """
    The :class:`ContextEncoder` class is the context encoder component of generative dialogue models,
    which encodes dialogue contexts into real-valued vectors.
    The real-valued vectors are usually considered the summary of multi-turn utterances.
    The :class:`ContextEncoder` class is implemented through a recurrent neural network.

    The typical shape of inputs is like ``[batch_size, seq_len]``.
    The shape of output vectors is like ``[batch_size, hidden_dim]``.
    """
    def __init__(self, params, input_keep_prob, name="context_encoder"):
        self._input_shape = tf.TensorShape([None, params.seq_len])
        self._output_shape = tf.TensorShape([None, params.hidden_dim])
        self._params = params
        self._input_keep_prob = input_keep_prob

        DeterministicComponent.__init__(self, name, self._input_shape, self._output_shape, tf.float32)


    def __call__(self, inputs, encoder_lengths):

        with tf.variable_scope("context_encoder") as scope:
            if self._params.encoder_type == "uni":
                encoder_cell = rnn_builder.create_rnn_cell(
                    self._params.cell_type, self._params.ctx_enc_dim, self._params.num_layers,
                    use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

                encoder_outputs, encoder_states = tf.nn.dynamic_rnn(
                    cell=encoder_cell, inputs=inputs,
                    sequence_length=encoder_lengths, dtype=tf.float32,
                    swap_memory=True)

                # gru: [batch_size, seq_len, hidden_size] [batch_size, hidden_size]
                # lstm: [batch_size, hidden_size] * num_layers
                return encoder_outputs, encoder_states

            elif self._params.encoder_type == "bi":

                fw_cell = rnn_builder.create_rnn_cell(
                    self._params.cell_type, self._params.hidden_units, self._params.num_layers,
                    use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

                bw_cell = rnn_builder.create_rnn_cell(
                    self._params.cell_type, self._params.hidden_units, self._params.num_layers,
                    use_residual=self._params.use_residual, input_keep_prob=self._input_keep_prob)

                encoder_outputs, encoder_states = tf.nn.bidirectional_dynamic_rnn(
                    cell_fw=fw_cell, cell_bw=bw_cell, inputs=inputs,
                    dtype=tf.float32, sequence_length=encoder_lengths, swap_memory=True)

                return encoder_outputs, encoder_states

            else:
                raise ValueError("Unknown encoder_type Error: %s" % self._params.encoder_type)