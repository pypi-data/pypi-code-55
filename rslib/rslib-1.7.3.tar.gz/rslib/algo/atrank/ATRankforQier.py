import os
import json
import numpy as np
import tensorflow as tf
from tensorflow_core.python import keras
from tensorflow_core.python.keras import layers, regularizers

from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.layers.interaction import BiInteractionPooling
from .ATRankLayer import ATRankLayer, PositionalEncoding

from ..utils import input_holder
from ..utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding
from ..utils.model_compile import compile_model


def get_model(config, return_session=False):
    '''
    get ATRank model
    https://arxiv.org/abs/1711.06632
    :param config:
    :return:
    '''
    activation = 'relu'
    hidden_unit = config['hidden_units']
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input], model_input = input_holder.getInput(config)

    user_feature = id_input_processing(user_feature_input, config)
    cross_feature = cross_input_processing(cross_feature_input, config)

    dense_all, time_mask_all = sequence_group_embedding(sequence_id_input, sequence_time_input, config)

    # seq_attention1 = ATRankLayer(config=config, type='encode')(dense_all, dense_all, mask=[time_mask_all, time_mask_all], learning_phase=K.learning_phase())
    # seq_attention1 = ATRankLayer(config=config, type='encode', name='x1')([dense_all, dense_all], mask=[time_mask_all, time_mask_all], learning_phase=K.learning_phase())
    # seq_embedding1 = layers.Lambda(lambda x: tf.reduce_mean(x, axis=1), name='attention1_reduce')(seq_attention1)

    seq_attention1 = tf.keras.layers.Attention()([dense_all, dense_all], mask=[time_mask_all > 0, time_mask_all > 0])
    seq_embedding1 = tf.keras.layers.GlobalAveragePooling1D()(seq_attention1, mask=time_mask_all > 0)

    all_feature = layers.Concatenate(axis=-1)([seq_embedding1, user_feature, cross_feature])

    all_feature = layers.Dense(hidden_unit * 4, activation='relu')(all_feature)
    all_feature = layers.Dropout(0.3)(all_feature)
    all_feature = layers.Dense(hidden_unit * 4, activation='relu')(all_feature)
    all_feature = layers.Dropout(0.4)(all_feature)

    output = layers.Dense(output_unit)(all_feature)

    output_layer = {
        'multi_class': tf.nn.softmax,
        'multi_label': tf.sigmoid,
        'regression': lambda x: x,
        'multi_regression': lambda x: x
    }[output_type]
    output = output
    output = output_layer(output)
    model = Model(inputs=model_input, outputs=[output])
    model, sess = compile_model(model, config)

    print(model.summary())
    if return_session:
        return model, sess
    else:
        return model
