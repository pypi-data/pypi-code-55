import tensorflow as tf
from deepdialog.utils import rnn_builder
from deepdialog.utils import attention_builder

from deepdialog.component.base import DeterministicComponent

__ALL__ = ['Decoder']

class Decoder(DeterministicComponent):
    """
    The :class:`Decoder` class defines the decoder component of generative dialogue models.
    It is implemented through a recurrent neural network.

    Parameters
    ----------
    embedding: an Tensorflow variable
        The vocabulary embedding.
    mode: string
        The working mode
    """
    def __init__(self, embedding, mode, params, decoder_keep_prob, name="decoder"):

        self._embedding = embedding
        self._mode = mode
        self._params = params
        self._decoder_keep_prob = decoder_keep_prob

        # self._input_shape = []
        # self._output_shape = []

        DeterministicComponent.__init__(self, name, [], [], tf.float32)


    def __call__(self, encoder_outputs,encoder_states, encoder_lengths, decoder_inputs, decoder_lengths):

        with tf.variable_scope("attention_decoder") as scope:

            decoder_cell, decoder_initial_state = self._prepare_decoder(
                encoder_outputs, encoder_states, encoder_lengths)

            output_layer = tf.layers.Dense(self._params.vocab_size,
                                           kernel_initializer=tf.truncated_normal_initializer(mean=0.0, stddev=0.1),
                                           _scope='decoder/dense')

            if self._mode != tf.contrib.learn.ModeKeys.INFER:  # train

                decoder_embedded_inputs = tf.nn.embedding_lookup(self._embedding, decoder_inputs)
                helper = tf.contrib.seq2seq.TrainingHelper(decoder_embedded_inputs, decoder_lengths, time_major=False)
                basic_decoder = tf.contrib.seq2seq.BasicDecoder(
                    decoder_cell, helper, decoder_initial_state, output_layer=output_layer)

                outputs, final_decoder_state, _ = tf.contrib.seq2seq.dynamic_decode(
                    basic_decoder, impute_finished=True, swap_memory=True, scope=scope)

                sample_id = outputs.sample_id
                logits = tf.identity(outputs.rnn_output)

            else:  # inference
                beam_width = self._params.beam_width
                start_tokens = tf.fill([self._params.batch_size], self._params.SOS_ID)
                end_token = self._params.EOS_ID

                decoding_length_factor = self._params.decoding_length_factor
                max_encoder_length = tf.reduce_max(encoder_lengths)
                maximum_iterations = tf.to_int32(tf.round(tf.to_float(max_encoder_length) * decoding_length_factor))

                if beam_width > 0:
                    infer_decoder = tf.contrib.seq2seq.BeamSearchDecoder(decoder_cell, self._embedding, start_tokens,
                                                                         end_token,
                                                                         initial_state=decoder_initial_state,
                                                                         beam_width=beam_width,
                                                                         output_layer=output_layer,
                                                                         length_penalty_weight=self._params.length_penalty_weight)
                else:
                    helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(self._embedding, start_tokens, end_token)
                    infer_decoder = tf.contrib.seq2seq.BasicDecoder(
                        decoder_cell,
                        helper,
                        decoder_initial_state,
                        output_layer=output_layer)

                outputs, final_decoder_state, _ = tf.contrib.seq2seq.dynamic_decode(
                    infer_decoder,
                    maximum_iterations=maximum_iterations,
                    swap_memory=True,
                    scope=scope)

                if beam_width > 0:
                    logits = tf.no_op()
                    sample_id = outputs.predicted_ids
                else:
                    logits = outputs.rnn_output
                    sample_id = outputs.sample_id

            return logits, sample_id, final_decoder_state


    def _prepare_decoder(self, encoder_outputs, encoder_states, encoder_lengths):

        decoder_cell = rnn_builder.create_rnn_cell(
            self._params.cell_type, self._params.hidden_dim, self._params.num_layers,
            use_residual=self._params.use_residual, input_keep_prob=self._decoder_keep_prob)

        if self._mode == tf.contrib.learn.ModeKeys.INFER and self._params.beam_width > 0:
            batch_size = self._params.batch_size * self._params.beam_width
            decoder_initial_state = tf.contrib.seq2seq.tile_batch(encoder_states, multiplier=self._params.beam_width)
            memory = tf.contrib.seq2seq.tile_batch(encoder_outputs, multiplier=self._params.beam_width)
            memory_lengths = tf.contrib.seq2seq.tile_batch(encoder_lengths, multiplier=self._params.beam_width)
        else:
            batch_size = self._params.batch_size
            decoder_initial_state = encoder_states
            memory = encoder_outputs
            memory_lengths = encoder_lengths

        if not self._params.use_attention:
            return decoder_cell, decoder_initial_state

        attention_mechanism = attention_builder.create_attention(self._params.attention_type, self._params.hidden_dim,
                                                                 memory,
                                                                 memory_lengths)
        alignment_history = (self._mode == tf.contrib.learn.ModeKeys.INFER and self._params.beam_width == 0)
        decoder_cell = tf.contrib.seq2seq.AttentionWrapper(decoder_cell,
                                                           attention_mechanism=attention_mechanism,
                                                           attention_layer_size=self._params.hidden_dim,
                                                           alignment_history=alignment_history,
                                                           output_attention=True,
                                                           name="vanilla_attention")

        decoder_initial_state = decoder_cell.zero_state(batch_size, tf.float32).clone(
            cell_state=decoder_initial_state)

        return decoder_cell, decoder_initial_state



