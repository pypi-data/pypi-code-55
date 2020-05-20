import tensorflow as tf
from deepdialog.model import AbstractModel
from deepdialog.component.encoder import Encoder
from deepdialog.component.encoder import ContextEncoder
from deepdialog.component.decoder import Decoder

from deepdialog.utils.register import Registers

@Registers.model.register
class HREDModel(AbstractModel):

    def __init__(self, params, mode, scope):
        AbstractModel.__init__(self, params, mode, scope)
        self.logits = None

    def prepare_io(self):
        self.encoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None, None), name="encoder_inputs")
        self.encoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None, None), name="encoder_lengths")
        self.decoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_inputs")
        self.decoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None,), name="decoder_lengths")
        self.decoder_targets = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_targets")

        self.batch_size = tf.shape(self.encoder_inputs)[0]
        self.dial_len = tf.shape(self.encoder_inputs)[1]
        self.cxt_enc_lens = tf.fill([self.batch_size], self.dial_len)

    def build_graph(self):
        with tf.variable_scope(self.scope or "hred", dtype=tf.float32):

            # utterance encoder
            self.utterance_encoder = Encoder(
                self.embeddings, self.params, self.encoder_keep_prob)
            utt_encoder_outputs, utt_encoder_states = self.utterance_encoder(self.encoder_inputs, self.encoder_lengths)
            # [batch_size * num_dial, hidden_dim]

            # context encoder
            cxt_inputs = tf.reshape(utt_encoder_states, [self.batch_size, self.dial_len, self.params.hidden_dim])
            self.context_encoder = ContextEncoder(self.params, input_keep_prob=1.0)
            cxt_encoder_outputs, cxt_encoder_states = self.context_encoder(
                cxt_inputs, self.cxt_enc_lens)

            # decoder
            self.decoder = Decoder(
                self.embeddings, self.mode, self.params, self.decoder_keep_prob)
            self.logits, sample_id, final_decoder_states = self.decoder(
                cxt_encoder_outputs, cxt_encoder_states, self.encoder_lengths,
                self.decoder_inputs, self.decoder_lengths)


    def prepare_loss(self):
        if self.mode == tf.contrib.learn.ModeKeys.INFER:
            self.loss = None
            self.other_losses = {}
        else: # train/eval

            """
            self.max_decoder_length = tf.reduce_max(self.decoder_lengths, name="max_decoder_length")
            self.mask = tf.sequence_mask(self.decoder_lengths, self.max_decoder_length, dtype=tf.float32, name='masks')
            loss = tf.contrib.seq2seq.sequence_loss(
                logits=self.logits, targets=self.decoder_targets, weights=self.mask)
            """

            cross_ent = tf.nn.sparse_softmax_cross_entropy_with_logits(
                labels=self.decoder_targets, logits=self.logits)

            max_time = self.decoder_targets.shape[1].value or tf.shape(self.decoder_targets)[1]
            target_weights = tf.sequence_mask(self.decoder_lengths, max_time, dtype=self.logits.dtype)
            batch_size = tf.size(self.decoder_lengths)
            loss = tf.reduce_sum(cross_ent * target_weights) / tf.to_float(batch_size)

            self.loss = loss
            self.other_losses["word_count"] = tf.reduce_sum(self.decoder_lengths)
            self.other_losses["nll"] = tf.reduce_sum(cross_ent * target_weights)
            self.other_losses["ppl"] = \
                tf.exp(tf.reduce_sum(cross_ent * target_weights)/tf.to_float(tf.reduce_sum(self.decoder_lengths)))


    def batch_2_feed(self, batch):
        encoder_inputs, encoder_lengths, decoder_inputs, decoder_lengths, decoder_targets = batch

        feed_dict = {
            self.encoder_inputs: encoder_inputs,
            self.encoder_lengths: encoder_lengths,
            self.decoder_inputs: decoder_inputs,
            self.decoder_lengths: decoder_lengths,
            self.decoder_targets: decoder_targets
        }
        return feed_dict