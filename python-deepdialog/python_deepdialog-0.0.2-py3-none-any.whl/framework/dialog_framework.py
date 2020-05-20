import time
import os
import tensorflow as tf
import numpy as np
from abc import abstractmethod

from deepdialog.utils.register import Registers


class Context(object):
    @classmethod
    def get_context_stack(cls):
        if not hasattr(cls, "_context_stack"):
            cls._context_stack = []
        return cls._context_stack

    @classmethod
    def get_context(cls):
        try:
            return cls.get_context_stack()[-1]
        except IndexError:
            raise RuntimeError("No contexts in the context_stack.")

    def __enter__(self):
        type(self).get_context_stack().append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        type(self).get_context_stack().pop()




class AbstractFramework(object):

    def __init__(self, model_name, model_params, scope, retrain=True, ckp_dir=None, word2vec=None):

        print(type(self))
        self._model_name = model_name
        self._model_params = model_params
        self._scope = scope
        self._retrain = retrain

        self._sess = tf.Session()

        with tf.variable_scope(scope, reuse=None):
            self._train_model = Registers.model[model_name](params=model_params, mode="train", scope=scope)
        with tf.variable_scope(scope, reuse=True):
            self._eval_model = Registers.model[model_name](params=model_params, mode="eval", scope=scope)
        with tf.variable_scope(scope, reuse=True):
            self._infer_model = Registers.model[model_name](params=model_params, mode="tests", scope=scope)

        self._word2vec = word2vec
        self._ckp_dir = ckp_dir
        if not os.path.exists(self._ckp_dir):
            os.mkdir(self._ckp_dir)

        self.prepare_model()


    def prepare_model(self):
        if self._word2vec is not None:
            print("Initializing word2vec")
            self._sess.run(self._train_model.embeddings.assign(np.array(self._word2vec)))

        ckpt = tf.train.latest_checkpoint(self._ckp_dir)
        if ckpt and (not self._retrain):
            self._train_model.saver.restore(self._sess, ckpt)
            print("Restoring train model parameters from %s" % ckpt)
        else:
            print("Creating new train model with fresh parameters.")
            self._sess.run(tf.global_variables_initializer())
            self._sess.run(tf.tables_initializer())


    """
    def prepare_test_model(self):
        ckpt = tf.train.latest_checkpoint(self._ckp_dir)
        if ckpt:
            with self._eval_model.graph.as_default():
                self._eval_model.saver.restore(self._sess, ckpt)
                print("Restoring tests model parameters from %s" % ckpt)
        else:
            raise FileNotFoundError("Not Found ckpt files.")

    def prepare_infer_model(self):
        ckpt = tf.train.latest_checkpoint(self._ckp_dir)
        if ckpt:
            with self._infer_model.graph.as_default():
                self._infer_model.saver.restore(self._sess, ckpt)
                print("Restoring infer model parameters from %s" % ckpt)
        else:
            raise FileNotFoundError("Not Found ckpt files.")
    """

    @abstractmethod
    def train(self, dataloader, max_num_epoch, step_limits):
        pass

    @abstractmethod
    def test(self, dataloader):
        pass

    @abstractmethod
    def interactive(self):
        pass




class DialogFramework(AbstractFramework, Context):
    def __init__(self, model_name, model_params, scope, ckp_dir, retrain=False, word2vec=None):
        AbstractFramework.__init__(self, model_name, model_params, scope, retrain, ckp_dir, word2vec)

    def train(self, dataloader, max_num_epoch, step_limits=5000):
        start_time = time.time()
        best_valid_loss = np.inf
        checkpoint_path_name = os.path.join(self._ckp_dir, self._train_model.__class__.__name__ + ".ckpt")
        for epoch in range(max_num_epoch):

            cur_lr = self._sess.run(self._train_model.learning_rate)
            cur_step = self._sess.run(self._train_model.global_step)
            print(" [*] Epoch: %d | Step: %d | Learning Rate: %f" % (epoch, cur_step, cur_lr))

            dataloader.shuffle()

            train_generator = dataloader.create_train_generator(self._model_params.batch_size)
            train_names, train_outputs = self._train_model.train(
                train_generator, self._sess, step_limits=step_limits)
            train_loss = train_outputs[0]

            valid_generator = dataloader.create_valid_generator(self._model_params.batch_size)
            valid_names, valid_outputs = self._eval_model.test(valid_generator, self._sess)
            valid_loss = valid_outputs[0]

            if valid_loss < best_valid_loss:
                print("[*] Save current model into %s." % checkpoint_path_name)
                self._train_model.saver.save(self._sess, checkpoint_path_name, global_step=epoch)
                best_valid_loss = valid_loss

            print("[*] train_loss: %.4f | valid_loss: %.4f | elapsed_time: %.4f" %
                  (train_loss, valid_loss, (time.time() - start_time)))
            print("\n")

        print("\n")
        print("Finish Training.")
        print("Best valid loss %.4f" % best_valid_loss)


    def test(self, dataloader):
        start_time = time.time()
        dataloader.shuffle()
        test_generator = dataloader.create_test_generator(batch_size=self._model_params.batch_size)
        eval_names, eval_outputs = self._eval_model.test(test_generator, self._sess)


    def interactive(self):
        pass






# todo to implement multi-task dialogue framework.
class MDialogFramework(AbstractFramework, Context):
    def __init__(self, model_name, model_config, scope, ckp_dir=None, word2vec=None):
        AbstractFramework.__init__(model_name, model_config, scope, ckp_dir, word2vec)
        pass

    def train(self, dataloader, max_num_epoch, step_limits):
        pass

    def test(self, dataloader):
        pass

    def interactive(self):
        pass