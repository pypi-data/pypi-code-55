import tensorflow as tf
from deepdialog.model.model_wrapper import TrainModel, EvalModel, InferModel
from deepdialog.model.vhred.vhred import VHREDModel


def create_vhred_train_model(dataset, dataloader, train_config, scope):
    train_data = dataloader.get_train_data()
    train_label_list = dataloader.get_train_label_list()
    train_generator = dataloader.get_generator(train_data, train_label_list)

    word2id = dataset.get_word2id()
    id2word = dataset.get_id2word()

    graph = tf.Graph()
    with graph.as_default():
        model = VHREDModel(train_config,
                           word2id,
                           id2word,
                           train_generator,
                           mode=tf.contrib.learn.ModeKeys.TRAIN,
                           scope=scope,
                           dtype=tf.float32)
    return TrainModel(
        graph=graph,
        model=model,
        iterator=train_generator)


def create_vhred_test_model(dataset, dataloader, test_config, scope):
    test_data = dataloader.get_test_data()
    test_label_list = dataloader.get_test_label_list()
    test_generator = dataloader.get_generator(test_data, test_label_list)

    word2id = dataset.get_word2id()
    id2word = dataset.get_id2word()

    graph = tf.Graph()
    with graph.as_default():
        test_model = VHREDModel(
            test_config,
            word2id,
            id2word,
            test_generator,
            mode=tf.contrib.learn.ModeKeys.EVAL,
            scope=scope,
            dtype=tf.float32)

    return EvalModel(
        graph=graph,
        model=test_model,
        iterator=test_generator)


def create_vhred_infer_model():
    pass
