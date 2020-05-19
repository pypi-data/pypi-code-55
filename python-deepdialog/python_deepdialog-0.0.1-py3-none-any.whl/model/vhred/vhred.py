import tensorflow as tf
from deepdialog.model.base_model import BaseModel
from deepdialog.component.encoder import encoder, context_encoder
from deepdialog.component.decoder import decoder
from deepdialog.component import variational_network
from deepdialog.evaluation.evaluator import gaussian_kld
from deepdialog.loss_function.loss import sparse_softmax_cross_entropy_with_logits


class VHREDModel(BaseModel):
    def __init__(self, params, word2id, id2word, iterator, mode, scope=None, dtype=tf.float32):
        super().__init__(params, word2id, id2word, mode, scope)

        self.sos_id = word2id["<sos>"]
        self.eos_id = word2id["<eos>"]
        self.mode = mode
        # self.iterator = iterator

        with tf.name_scope("io"):
            self.encoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None, None), name="encoder_inputs")
            self.encoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None, None), name="encoder_lengths")
            self.decoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_inputs")
            self.decoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None,), name="decoder_lengths")
            self.decoder_targets = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_targets")

            batch_size = tf.shape(self.encoder_inputs)[0]
            encoder_utt_num = tf.shape(self.encoder_inputs)[1]
            encoder_utt_len = tf.shape(self.encoder_inputs)[2]

        with tf.variable_scope(scope or "vhred", dtype=dtype):
            # response_encoder
            with tf.variable_scope("response_encoder"):
                if mode == tf.contrib.learn.ModeKeys.INFER:
                    response_states = None
                else:
                    _, response_states = encoder(self.mask_embeddings, self.decoder_targets,
                                                          self.decoder_lengths, params, self.encoder_keep_prob)
                # response_states: (batch_size, utt_enc_dim) * num_layers

            # utterance_encoder
            with tf.variable_scope("utterance_encoder"):
                utt_enc_inputs = tf.reshape(self.encoder_inputs,
                                            [batch_size * encoder_utt_num,
                                             encoder_utt_len])  # (batch_size*utt_num, utt_len)
                utt_enc_lens = tf.reshape(self.encoder_lengths, [batch_size * encoder_utt_num, ])
                utt_encoder_outputs, utt_encoder_states = encoder(self.mask_embeddings, utt_enc_inputs,
                                                                  utt_enc_lens, self.params,
                                                                  self.encoder_keep_prob)
                # utt_enc_states: (batch_size*utt_num, utt_enc_dim)* num_layers

            # context_encoder
            with tf.variable_scope("context_encoder"):
                ctx_enc_inputs = tf.layers.dense(inputs=utt_encoder_states,
                                                 units=params.ctx_enc_dim, activation=tf.tanh, name="utt_states2ctx_inputs")
                ctx_enc_inputs = tf.reshape(ctx_enc_inputs, [batch_size, encoder_utt_num, params.ctx_enc_dim])
                ctx_enc_lens = tf.fill([batch_size], encoder_utt_num)
                ctx_enc_outputs, ctx_enc_states = context_encoder(ctx_enc_inputs,
                                                                  ctx_enc_lens, params, self.encoder_keep_prob)
            # ctx_enc_states: (batch_size, ctx_enc_dim)

            # variation_network
            if mode == tf.contrib.learn.ModeKeys.TRAIN:
                prior_mu, prior_logvar = variational_network.prior(ctx_enc_states, params)
                posterior_mu, posterior_logvar = variational_network.posterior(ctx_enc_states, response_states, params)
                latent_sample = variational_network.sample_gaussian(posterior_mu, posterior_logvar)

            elif mode == tf.contrib.learn.ModeKeys.EVAL:
                prior_mu, prior_logvar = variational_network.prior(ctx_enc_states, params)
                posterior_mu, posterior_logvar = variational_network.posterior(ctx_enc_states, response_states, params)
                latent_sample = variational_network.sample_gaussian(prior_mu, prior_logvar)
            elif mode == tf.contrib.learn.ModeKeys.INFER:
                prior_mu, prior_logvar = variational_network.prior(ctx_enc_states, params)
                posterior_mu, posterior_logvar = None, None
                latent_sample = variational_network.sample_gaussian(prior_mu, prior_logvar)
            else:
                raise ValueError("valid mode")

            self.latent_sample = latent_sample
            concat_states = tf.concat([ctx_enc_states, latent_sample], -1)

            # decoder
            ctx_enc_outputs = tf.layers.dense(inputs=ctx_enc_outputs,
                                              units=params.hidden_units, activation=tf.tanh, name="ctx_outputs2decoder")
            concat_states = tf.layers.dense(inputs=concat_states,
                                            units=params.hidden_units, activation=tf.tanh, name="concat_states2decoder")
            logits, sample_id, final_decoder_states = decoder(
                self.mask_embeddings, ctx_enc_outputs, concat_states,
                self.encoder_lengths, self.decoder_inputs,
                self.decoder_lengths, self.mode, self.params, self.decoder_keep_prob)

            if mode == tf.contrib.learn.ModeKeys.TRAIN:
                self.predict_count = tf.reduce_sum(self.decoder_lengths)
                self.rc_loss = self._compute_loss(logits, self.decoder_targets, self.decoder_lengths)
                kl_weights = tf.minimum(tf.to_float(self.global_t) / params.full_kl_step, 1.0)
                self.kl_loss = tf.reduce_mean(gaussian_kld(posterior_mu, posterior_logvar, prior_mu, prior_logvar))
                self.elbo = self.rc_loss + kl_weights * self.kl_loss
                self.train_loss = self.elbo
                self.prepare_optimize(self.elbo)
            elif mode == tf.contrib.learn.ModeKeys.EVAL:
                self.predict_count = tf.reduce_sum(self.decoder_lengths)
                self.rc_loss = self._compute_loss(logits, self.decoder_targets, self.decoder_lengths)
                kl_weights = kl_weights = tf.constant(1.0)
                self.kl_loss = tf.reduce_mean(gaussian_kld(posterior_mu, posterior_logvar, prior_mu, prior_logvar))
                self.elbo = self.rc_loss + kl_weights * self.kl_loss
                self.eval_loss = self.elbo
            elif mode == tf.contrib.learn.ModeKeys.INFER:
                self.rc_loss = None
                self.kl_loss = None
                self.elbo = None
                self.infer_logits, self.sample_id = logits, sample_id
            else:
                raise ValueError("valid mode")

            self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=3)

    @staticmethod
    def _compute_loss(logits, decoder_target, decoder_lengths):

        # print(logits)
        # print(decoder_target)

        cross_ent = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=decoder_target, logits=logits)
        """
        max_time = dec_outputs.shape[1].value or tf.shape(dec_outputs)[1]
        batch_size = dec_outputs.shape[0].value or tf.shape(dec_outputs)[0]
        weights = tf.sequence_mask(dec_lengths, max_time, dtype=logits.dtype)
        """
        max_time = decoder_target.shape[1].value or tf.shape(decoder_target)[1]
        target_weights = tf.sequence_mask(decoder_lengths, max_time, dtype=logits.dtype)
        batch_size = tf.size(decoder_lengths)
        loss = tf.reduce_sum(cross_ent * target_weights) / tf.to_float(batch_size)
        return loss

    def train(self, sess, batch_data):
        assert self.mode == tf.contrib.learn.ModeKeys.TRAIN

        # print(len(batch_data))
        # print(batch_data)

        feed_dict = {
            self.encoder_inputs: batch_data[0],
            self.encoder_lengths: batch_data[1],
            self.decoder_inputs: batch_data[2],
            self.decoder_lengths: batch_data[3],
            self.decoder_targets: batch_data[4],
        }
        return sess.run([self.train_ops, self.train_loss,
                         self.elbo, self.rc_loss,
                         self.kl_loss, self.predict_count,
                         self.train_summary, self.global_t,
                         # self.batch_size,
                         # self.grad_norm,
                         self.learning_rate], feed_dict)

    def test(self, sess, batch_data):
        assert self.mode == tf.contrib.learn.ModeKeys.EVAL
        feed_dict = {
            self.encoder_inputs: batch_data[0],
            self.encoder_lengths: batch_data[1],
            self.decoder_inputs: batch_data[2],
            self.decoder_lengths: batch_data[3],
            self.decoder_targets: batch_data[4],
        }
        return sess.run([self.eval_loss, self.elbo, self.rc_loss, self.kl_loss,
                         self.predict_count], feed_dict)

    def interactive(self, sess, batch_data):
        assert self.mode == tf.contrib.learn.ModeKeys.INFER
        feed_dict = {
            self.encoder_inputs: batch_data[0],
            self.encoder_lengths: batch_data[1],
            self.decoder_inputs: batch_data[2],
            self.decoder_lengths: batch_data[3],
            self.decoder_targets: batch_data[4],
        }
        return sess.run([
            self.infer_logits, self.sample_id
        ], feed_dict)
