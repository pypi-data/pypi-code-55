import os
import time
import tensorflow as tf
import numpy as np
from deepdialog.model.kgcvae import kgcvae_wrapper
from deepdialog.data_utils.dataset import KGCVAEDataset
from deepdialog.data_utils.data_loader import KGCVAEDataLoader
from deepdialog.model import model_helper


class DataLoaderConfig:
    batch_size = 8
    train_valid_split = 0.6
    valid_test_split = 0.8
    tokenized = True
    max_dialog_size = 3
    max_utterance_length = 8


class DatasetConfig:
    utterance_separator = "__eou__"
    dataset_name = "dailydialog"
    max_vocab_size = 20000
    max_dialog_size = 3


class ModelConfig:
    hidden_units = 3
    ctx_enc_dim = 2
    embed_size = 4
    latent_size = 2
    init_lr = 0.001
    lr_decay = 0.5
    encoder_type = "uni"
    cell_type = "gru"
    num_layers = 1
    use_residual = False
    batch_size = 8
    use_attention = False
    attention_type = "luong"
    vocab_size = 20000
    encoder_dropout_rate = 0.0
    decoder_dropout_rate = 0.0
    op = "adam"
    grad_clip = 5.0
    grad_noise = 0.0
    epochs = 3
    full_kl_step = 10000
    topic_embed_size = 2
    act_embed_size = 2
    bow_fc1_size = 3
    act_fc1_size = 3
    discriminator_keep_prob = 1.0


class KGCVAERunner(object):
    def __init__(self):
        dataset_config = DatasetConfig()
        self.dataset = dataset = KGCVAEDataset(dataset_config)

        cleaned_texts = dataset.get_cleaned_texts()
        label_list = dataset.get_raw_label_list()
        word2id = dataset.get_word2id()
        id2word = dataset.get_id2word()
        label2id_list = dataset.get_label2id_list()
        id2label_list = dataset.get_id2label_list()
        label_name_list = dataset.get_label_name_list()
        acts = dataset.get_acts()
        act2id = dataset.get_act2id()
        id2act = dataset.get_id2act()

        data_loader_config = DataLoaderConfig()
        self.dataloader = dataloader = KGCVAEDataLoader(
            data_loader_config, cleaned_texts, label_list, word2id, id2word,
            label2id_list, id2label_list, label_name_list, acts, act2id, id2act)

        self.model_config = ModelConfig()
        self.test_config = ModelConfig()

        self.out_dir = "../../kgcvae_save"
        self.model_dir = "../../kgcvae_save"

        self.eval_model = kgcvae_wrapper.create_vhred_test_model(
            dataset, dataloader, self.test_config, scope="kgcvae")
        self.train_model = kgcvae_wrapper.create_vhred_train_model(
            dataset, dataloader, self.model_config, scope="kgcvae")

        self.eval_sess = tf.Session(graph=self.eval_model.graph)
        self.train_sess = tf.Session(graph=self.train_model.graph)

    def train(self):
        with self.train_model.graph.as_default():
            loaded_train_model, global_step = model_helper.create_or_load_model(
                self.train_model.model, self.model_dir, self.train_sess, "train")
        """
        summary_writer = tf.summary.FileWriter(
            os.path.join(self.out_dir, "train_log"), self.train_model.graph)
        """
        for epoch in range(self.model_config.epochs):
            start_time = time.time()
            # print(epoch)
            train_loss_list = []
            elbo_list = []
            rc_loss_list = []
            kl_loss_list = []
            bow_loss_list = []
            act_loss_list = []
            for _, batch_data in enumerate(self.train_model.iterator()):
                step_result = loaded_train_model.train(self.train_sess, batch_data)
                _, train_loss, elbo, rc_loss, kl_loss, predict_count, \
                bow_loss, act_loss, train_summary, global_t, learning_rate = step_result
                train_loss_list.append(train_loss)
                elbo_list.append(elbo)
                rc_loss_list.append(rc_loss)
                kl_loss_list.append(kl_loss)
                bow_loss_list.append(bow_loss)
                act_loss_list.append(act_loss)
            print("Epoch %d/%d" % (epoch + 1, self.model_config.epochs))
            print("avg train loss: %f, elbo: %f, avg rc loss: %f, avg kl loss: %f, avg bow loss: %f, avg act loss: %f"
                  % (np.mean(train_loss_list), np.mean(elbo_list), np.mean(rc_loss_list), np.mean(kl_loss_list),
                     np.mean(bow_loss_list), np.mean(act_loss_list)))
            print()
        print("train done")

        loaded_train_model.saver.save(
            self.train_sess,
            os.path.join(self.out_dir, "kgcvae.ckpt"),
            global_step=global_step)

    def test(self):
        with self.eval_model.graph.as_default():
            loaded_eval_model, global_step = model_helper.create_or_load_model(
                self.eval_model.model, self.model_dir, self.eval_sess, "eval")
        """
        summary_writer = tf.summary.FileWriter(
            os.path.join(self.out_dir, "train_log"), self.train_model.graph)
        """
        eval_loss_list = []
        elbo_list = []
        rc_loss_list = []
        kl_loss_list = []
        bow_loss_list = []
        act_loss_list = []
        for _, batch_data in enumerate(self.eval_model.iterator()):
            eval_loss, elbo, rc_loss, kl_loss, predict_count, bow_loss, act_loss = loaded_eval_model.test(
                self.eval_sess,
                batch_data)
            eval_loss_list.append(eval_loss)
            elbo_list.append(elbo)
            rc_loss_list.append(rc_loss)
            kl_loss_list.append(kl_loss)
            bow_loss_list.append(bow_loss)
            act_loss_list.append(act_loss)
        print("avg eval loss: %f, elbo: %f, avg rc loss: %f, avg kl loss: %f, avg bow loss: %f, avg act loss: %f"
              % (np.mean(eval_loss_list), np.mean(elbo_list), np.mean(rc_loss_list), np.mean(kl_loss_list),
                 np.mean(bow_loss_list), np.mean(act_loss_list)))
        print("eval done")

    def interactive(self):
        pass
