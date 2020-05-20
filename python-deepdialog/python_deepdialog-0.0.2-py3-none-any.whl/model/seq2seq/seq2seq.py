import tensorflow as tf
from deepdialog.model import AbstractModel
from deepdialog.component.encoder import Encoder
from deepdialog.component.decoder import Decoder

from deepdialog.utils.register import Registers


@Registers.model.register("Seq2SeqModel")
class Seq2SeqModel(AbstractModel):

    def __init__(self, params, mode, scope):
        AbstractModel.__init__(self, params, mode, scope)

        # define losses
        self.logits = None
        self.predict_word_count = None

    def prepare_io(self):
        self.encoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None), name="encoder_inputs")
        self.encoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None,), name="encoder_lengths")
        self.decoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_inputs")
        self.decoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None,), name="decoder_lengths")
        self.decoder_targets = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_targets")

    def build_graph(self):
        with tf.variable_scope(self.scope or "seq2seq", dtype=tf.float32):
            self.seq2seq_encoder = Encoder(
                self.embeddings, self.params, self.encoder_keep_prob)

            encoder_outputs, encoder_states = self.seq2seq_encoder(self.encoder_inputs, self.encoder_lengths)

            self.seq2seq_decoder = Decoder(
                self.embeddings, self.mode, self.params, self.decoder_keep_prob)

            self.logits, sample_id, final_decoder_states = self.seq2seq_decoder(
                encoder_outputs, encoder_states, self.encoder_lengths,
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