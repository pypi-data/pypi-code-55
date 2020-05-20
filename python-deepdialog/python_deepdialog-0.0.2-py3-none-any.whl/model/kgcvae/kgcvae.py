import tensorflow as tf
from deepdialog.model.base_model import BaseModel
from deepdialog.component.encoder import encoder, context_encoder
from deepdialog.component.decoder import decoder
from deepdialog.component import variational_network
from deepdialog.component.discriminator import discriminator
from deepdialog.evaluation.evaluator import gaussian_kld
from deepdialog.loss_function.loss import sparse_softmax_cross_entropy_with_logits


class KGCVAEModel(BaseModel):
    def __init__(self, params, word2id, id2word, topic_size, act_size, iterator, mode, scope=None, dtype=tf.float32):
        super().__init__(params, word2id, id2word, mode, scope)

        self.sos_id = word2id["<sos>"]
        self.eos_id = word2id["<eos>"]
        self.mode = mode
        self.vocab_size = len(word2id)
        self.act_size = act_size
        # self.iterator = iterator

        with tf.name_scope("io"):
            self.encoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None, None), name="encoder_inputs")
            self.encoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None, None), name="encoder_lengths")
            self.decoder_inputs = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_inputs")
            self.decoder_lengths = tf.placeholder(dtype=tf.int32, shape=(None,), name="decoder_lengths")
            self.decoder_targets = tf.placeholder(dtype=tf.int32, shape=(None, None), name="decoder_targets")
            self.topics = tf.placeholder(dtype=tf.int32, shape=(None,), name="topics")
            self.acts = tf.placeholder(dtype=tf.int32, shape=(None,), name="acts")
            self.floors = tf.placeholder(dtype=tf.int32, shape=(None, None), name="floors")

            batch_size = tf.shape(self.encoder_inputs)[0]
            encoder_utt_num = tf.shape(self.encoder_inputs)[1]
            encoder_utt_len = tf.shape(self.encoder_inputs)[2]
            decoder_utt_len = tf.shape(self.decoder_targets)[1]

        with tf.variable_scope(scope or "kgcvae", dtype=dtype):
            # topic embedding
            with tf.variable_scope("topic_embedding"):
                topic_embedding = tf.get_variable("embedding", [topic_size, params.topic_embed_size],
                                                  dtype=tf.float32)
                embed_topic = tf.nn.embedding_lookup(topic_embedding, self.topics)

            # act embedding
            with tf.variable_scope("act_embedding"):
                act_embedding = tf.get_variable("embedding", [act_size, params.act_embed_size],
                                                dtype=tf.float32)
                embed_act = tf.nn.embedding_lookup(act_embedding, self.acts)

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
                # convert floors into 1 hot
                floor_one_hot = tf.one_hot(tf.reshape(self.floors, [-1]), depth=2, dtype=tf.float32)
                floor_one_hot = tf.reshape(floor_one_hot, [batch_size * encoder_utt_num, 2])
                utt_states_floor = tf.concat([utt_encoder_states, floor_one_hot], -1, "utt_states_floor")
                ctx_enc_inputs = tf.layers.dense(inputs=utt_states_floor,
                                                 units=params.ctx_enc_dim, activation=tf.tanh,
                                                 name="utt_states2ctx_inputs")
                ctx_enc_inputs = tf.reshape(ctx_enc_inputs, [batch_size, encoder_utt_num, params.ctx_enc_dim])
                ctx_enc_lens = tf.fill([batch_size], encoder_utt_num)
                ctx_enc_outputs, ctx_enc_states = context_encoder(ctx_enc_inputs,
                                                                  ctx_enc_lens, params, self.encoder_keep_prob)
            # ctx_enc_states: (batch_size, ctx_enc_dim)

            # variation_network
            if mode == tf.contrib.learn.ModeKeys.TRAIN:
                prior_joint_states = tf.concat([ctx_enc_states, embed_topic], -1)
                posterior_joint_states = tf.concat([ctx_enc_states, embed_topic, embed_act], -1)
                prior_mu, prior_logvar = variational_network.prior(prior_joint_states, params)
                posterior_mu, posterior_logvar = variational_network.posterior(posterior_joint_states, response_states,
                                                                               params)
                latent_sample = variational_network.sample_gaussian(posterior_mu, posterior_logvar)

            elif mode == tf.contrib.learn.ModeKeys.EVAL:
                prior_joint_states = tf.concat([ctx_enc_states, embed_topic], -1)
                posterior_joint_states = tf.concat([ctx_enc_states, embed_topic, embed_act], -1)
                prior_mu, prior_logvar = variational_network.prior(prior_joint_states, params)
                posterior_mu, posterior_logvar = variational_network.posterior(posterior_joint_states, response_states,
                                                                               params)
                latent_sample = variational_network.sample_gaussian(prior_mu, prior_logvar)
            elif mode == tf.contrib.learn.ModeKeys.INFER:
                prior_joint_states = tf.concat([ctx_enc_states, embed_topic], -1)
                posterior_joint_states = None
                prior_mu, prior_logvar = variational_network.prior(prior_joint_states, params)
                posterior_mu, posterior_logvar = None, None
                latent_sample = variational_network.sample_gaussian(prior_mu, prior_logvar)
            else:
                raise ValueError("valid mode")

            self.latent_sample = latent_sample
            concat_states = tf.concat([ctx_enc_states, embed_topic, latent_sample], -1)


            with tf.variable_scope("bow_discriminator"):
                # BOW
                bow_logits = discriminator(inputs=concat_states,
                                           label_size=self.vocab_size,
                                           keep_prob=params.discriminator_keep_prob,
                                           middle_units=params.bow_fc1_size)
                tile_bow_logits = tf.tile(tf.expand_dims(bow_logits, 1), [1, decoder_utt_len - 1, 1])
                bow_targets = self.decoder_inputs[:, 1:]  # delete <sos>
                bow_mask = tf.to_float(tf.sign(bow_targets))
            with tf.variable_scope("act_discriminator"):
                # act
                act_logits = discriminator(inputs=concat_states,
                                           label_size=self.act_size,
                                           keep_prob=params.discriminator_keep_prob, middle_units=params.act_fc1_size)
                act_prob = tf.nn.softmax(act_logits)
                pred_embed_act = tf.matmul(act_prob, act_embedding)
                if mode == tf.contrib.learn.ModeKeys.TRAIN:
                    selected_embed_act = embed_act
                else:
                    selected_embed_act = pred_embed_act

            # decoder
            gen_input = tf.concat([concat_states, selected_embed_act], -1)
            ctx_enc_outputs = tf.layers.dense(inputs=ctx_enc_outputs,
                                              units=params.hidden_units, activation=tf.tanh, name="ctx_outputs2decoder")
            gen_input = tf.layers.dense(inputs=gen_input,
                                        units=params.hidden_units, activation=tf.tanh, name="concat_states2decoder")
            logits, sample_id, final_decoder_states = decoder(
                self.mask_embeddings, ctx_enc_outputs, gen_input,
                self.encoder_lengths, self.decoder_inputs,
                self.decoder_lengths, self.mode, self.params, self.decoder_keep_prob)

            # loss
            if mode == tf.contrib.learn.ModeKeys.TRAIN:
                # elbo
                self.predict_count = tf.reduce_sum(self.decoder_lengths)
                self.rc_loss = self._compute_loss(logits, self.decoder_targets, self.decoder_lengths)
                kl_weights = tf.minimum(tf.to_float(self.global_t) / params.full_kl_step, 1.0)
                self.kl_loss = tf.reduce_mean(gaussian_kld(posterior_mu, posterior_logvar, prior_mu, prior_logvar))
                self.elbo = self.rc_loss + kl_weights * self.kl_loss
                # bow
                self.avg_bow_loss = self._discriminator_loss(logits=tile_bow_logits, labels=bow_targets,
                                                             dim_size=3, mask=bow_mask)
                # act
                self.avg_act_loss = self._discriminator_loss(logits=act_logits, labels=self.acts, dim_size=2)

                self.train_loss = self.elbo + self.avg_bow_loss + self.avg_act_loss
                self.prepare_optimize(self.train_loss)
            elif mode == tf.contrib.learn.ModeKeys.EVAL:
                self.predict_count = tf.reduce_sum(self.decoder_lengths)
                self.rc_loss = self._compute_loss(logits, self.decoder_targets, self.decoder_lengths)
                kl_weights = kl_weights = tf.constant(1.0)
                self.kl_loss = tf.reduce_mean(gaussian_kld(posterior_mu, posterior_logvar, prior_mu, prior_logvar))
                self.elbo = self.rc_loss + kl_weights * self.kl_loss
                # bow
                self.avg_bow_loss = self._discriminator_loss(logits=tile_bow_logits, labels=bow_targets,
                                                             dim_size=3, mask=bow_mask)
                # act
                self.avg_act_loss = self._discriminator_loss(logits=act_logits, labels=self.acts, dim_size=2)

                self.eval_loss = self.elbo + self.avg_bow_loss + self.avg_act_loss
            elif mode == tf.contrib.learn.ModeKeys.INFER:
                self.rc_loss = None
                self.kl_loss = None
                self.elbo = None
                self.avg_bow_loss = None
                self.avg_act_loss = None
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

    @staticmethod
    def _discriminator_loss(logits, labels, dim_size=2, mask=None):
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels)
        if mask is not None:
            loss = loss * mask
        if dim_size == 3:
            loss = tf.reduce_sum(loss, reduction_indices=1)
        return tf.reduce_mean(loss)

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
            self.topics: batch_data[5],
            self.acts: batch_data[6],
            self.floors: batch_data[7]
        }
        return sess.run([self.train_ops, self.train_loss,
                         self.elbo, self.rc_loss,
                         self.kl_loss, self.predict_count, self.avg_bow_loss, self.avg_act_loss,
                         self.train_summary, self.global_t,
                         self.learning_rate], feed_dict)

    def test(self, sess, batch_data):
        assert self.mode == tf.contrib.learn.ModeKeys.EVAL
        feed_dict = {
            self.encoder_inputs: batch_data[0],
            self.encoder_lengths: batch_data[1],
            self.decoder_inputs: batch_data[2],
            self.decoder_lengths: batch_data[3],
            self.decoder_targets: batch_data[4],
            self.topics: batch_data[5],
            self.acts: batch_data[6],
            self.floors: batch_data[7]
        }
        return sess.run([self.eval_loss, self.elbo, self.rc_loss, self.kl_loss,
                         self.predict_count, self.avg_bow_loss, self.avg_act_loss], feed_dict)

    def interactive(self, sess, batch_data):
        assert self.mode == tf.contrib.learn.ModeKeys.INFER
        pass
