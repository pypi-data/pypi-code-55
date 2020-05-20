import time
from abc import abstractmethod
import numpy as np
import re
import tensorflow as tf



class AbstractModel(object):
    def __init__(self, params, mode, scope=None):

        self.params = params
        self.mode = mode
        self.scope = scope

        self.embeddings = None
        self.params_size = None
        self.train_ops = None
        self.learning_rate = tf.Variable(float(params.init_lr), trainable=False, name="learning_rate")
        self.global_step = tf.Variable(0, dtype=tf.int32, name="global_step")
        self.encoder_keep_prob = 1.0
        self.decoder_keep_prob = 1.0


        self.loss = None
        self.other_losses = {}

        self.init_embeddings(params.vocab_size, params.embed_dim)
        self.get_keep_probs(mode, params.encoder_dropout_rate, params.decoder_dropout_rate)
        self.prepare_io()
        self.build_graph()
        self.prepare_loss()

        if self.scope is None:
            self.tvars = tf.trainable_variables()
        else:
            self.tvars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.scope)

        if self.mode == tf.contrib.learn.ModeKeys.TRAIN:
            self.prepare_optimizer(self.tvars, self.loss,
                                   params.optimizer_type,
                                   params.init_lr,
                                   params.grad_clip,
                                   params.grad_noise)

        self.saver = tf.train.Saver(tf.global_variables())

    def init_embeddings(self, vocab_size, embed_dim, scope=None):
        with tf.variable_scope(scope or "embeddings", dtype=tf.float32):
            embeddings = tf.get_variable("trainable_embeddings",
                                         shape=[vocab_size, embed_dim],
                                         trainable=True,
                                         dtype=tf.float32)
            embedding_mask = tf.constant(
                [0 if i == 0 else 1 for i in range(vocab_size)], dtype=tf.float32, shape=[vocab_size, 1])
            self.embeddings = embeddings * embedding_mask

    def get_keep_probs(self, mode, encoder_dropout_rate, decoder_dropout_rate):
        if mode == tf.contrib.learn.ModeKeys.TRAIN:
            encoder_keep_prob = 1.0 - encoder_dropout_rate
            decoder_keep_prob = 1.0 - decoder_dropout_rate
        else:
            encoder_keep_prob = 1.0
            decoder_keep_prob = 1.0
        self.encoder_keep_prob = encoder_keep_prob
        self.decoder_keep_prob = decoder_keep_prob

    """
    def update_decay_learning_rate(self, cur_step, cur_lr, lr_decay_scheme, num_train_steps):

        if lr_decay_scheme == "luong10":
            start_decay_step = int(num_train_steps / 2)
            remain_steps = num_train_steps - start_decay_step
            decay_steps = int(remain_steps / 10)  # decay 10 times
            decay_factor = 0.5
        elif lr_decay_scheme == "luong234":
            start_decay_step = int(num_train_steps * 2 / 3)
            remain_steps = num_train_steps - start_decay_step
            decay_steps = int(remain_steps / 4)  # decay 4 times
            decay_factor = 0.5
        else: # do not decay
            start_decay_step = num_train_steps
            decay_steps = 0
            decay_factor = 1.0

        print(" [*] lr_decay_scheme=%s, start_decay_step=%d, decay_steps %d, decay_factor %g" %
              (lr_decay_scheme, start_decay_step, decay_steps, decay_factor))

        if cur_step < start_decay_step:
            ret = tf.convert_to_tensor(cur_lr, tf.float32)
        else:
            ret = tf.train.exponential_decay(
                cur_lr, (cur_step - start_decay_step), decay_steps, decay_factor, staircase=True)
        return ret
    """

    def print_model_size(self, tvars):
        total_parameters = 0
        for variable in tvars:
            # shape is an array of tf.Dimension
            shape = variable.get_shape()
            variable_parameters = 1
            for dim in shape:
                variable_parameters *= dim.value
            print("Trainable %s with %d parameters" % (variable.name, variable_parameters))
            total_parameters += variable_parameters
        print("Total number of trainable parameters is %d" % total_parameters)
        self.params_size = total_parameters

    @staticmethod
    def print_loss(prefix, loss_names, losses, postfix):
        template = "%s "
        for name in loss_names:
            template += "%s: " % name
            template += " %f | "
        template += "%s"
        template = re.sub(' +', ' ', template)
        avg_losses = []
        values = [prefix]

        for loss in losses:
            values.append(np.mean(loss))
            avg_losses.append(np.mean(loss))
        values.append(postfix)

        print(template % tuple(values))

    @abstractmethod
    def build_graph(self):
        pass

    @abstractmethod
    def prepare_io(self):
        pass

    @abstractmethod
    def prepare_loss(self):
        pass


    def prepare_optimizer(self, tvars, loss, optimizer_type, init_lr, grad_clip=5.0, grad_noise=0.0):

        if optimizer_type.lower() == "adam":
            print("Use AdamOptimizer")
            optimizer = tf.train.AdamOptimizer(init_lr)
        elif optimizer_type.lower() == "rmsprop":
            print("Use RMSPropOptimizer")
            optimizer = tf.train.RMSPropOptimizer(init_lr)
        elif optimizer_type.lower() == "sgd":
            print("Use SGDOptimizer")
            optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        else:
            raise ValueError("optimizer_type only accept values from [Adam, rmsprop, sgd]")

        gradients = tf.gradients(
            loss, tvars, colocate_gradients_with_ops=True)

        clipped_grads, grad_norm = tf.clip_by_global_norm(gradients, tf.constant(grad_clip))

        # add gradient noise
        if grad_noise > 0:
            grad_std = tf.sqrt(grad_noise / tf.pow(1.0 + tf.to_float(self.global_step), 0.55))
            clipped_grads = [g + tf.truncated_normal(tf.shape(g), mean=0.0, stddev=grad_std) for g in clipped_grads]

        self.train_ops = optimizer.apply_gradients(zip(clipped_grads, tvars),
                                                   global_step=self.global_step)
        self.print_model_size(tvars)


    @abstractmethod
    def batch_2_feed(self, batch):
        pass


    def train(self, generator, sess, step_limits):
        local_t = 0
        start_time = time.time()

        output_names = ["loss"] + list(self.other_losses.keys())
        output_values = []
        for _ in range(len(output_names)):
            output_values.append(list())

        while True:
            try:
                batch = next(generator)
            except StopIteration:
                break
            if step_limits is not None and local_t >= step_limits:
                break
            feed_dict = self.batch_2_feed(batch)
            fetches = [self.train_ops, self.loss] + list(self.other_losses.values())
            results = sess.run(fetches, feed_dict)

            print(results)
            for idx, res in enumerate(results[1:]):
                output_values[idx].append(res)

            local_t += 1
            if local_t % 500 == 0:
                outs = [np.mean(item) for item in output_values]
                self.print_loss("", output_names, outs, "")

        epoch_time = time.time() - start_time
        print("\n")
        final_outs = [np.mean(item) for item in output_values]
        self.print_loss("Train Epoch:", output_names, final_outs, postfix="epoch_time: %.4f"%epoch_time)

        return output_names, final_outs


    def test(self, generator, sess):
        start_time = time.time()
        output_names = ["loss"] + list(self.other_losses.keys())
        output_values = []
        for _ in range(len(output_names)):
            output_values.append(list())

        while True:
            try:
                batch = next(generator)
            except StopIteration:
                break
            feed_dict = self.batch_2_feed(batch)
            fetches = [self.loss] + list(self.other_losses.values())
            results = sess.run(fetches, feed_dict)

            for idx, res in enumerate(results):
                output_values[idx].append(res)

            #print(output_values)

        epoch_time = time.time() - start_time
        print("\n")
        final_outs = [np.mean(item) for item in output_values]
        self.print_loss("Test Results:", output_names, final_outs, postfix="test_time: %.4f"%epoch_time)
        return output_names, final_outs