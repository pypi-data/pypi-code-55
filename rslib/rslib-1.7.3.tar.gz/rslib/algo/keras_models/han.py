#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
keras_han

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import tensorflow as tf

from tensorflow.python.keras import layers, regularizers
from tensorflow.python.keras.backend import _constant_to_tensor, epsilon
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K
from ..transformer.Attention import Attention, Attention2
from rslib.algo.layers.interaction import BiInteractionPooling
from rslib.core.LossUtil import masked_categorical_crossentropy, zzn_loss
from ..sparse_dnn.DenseLayerForSparse import DenseLayerForSparse

# class MyModel(tf.keras.Model):
#     def __init__(self, config):
#         self.supports_masking = False
#         self.config = config
#         super(MyModel, self).__init__()
#
#     def call(self, x, mask=None):
#         embeddings = x[0]
#         maxlen = self.config['maxlen']
#
#         time_distributed_input = layers.Input(shape=(2, maxlen,), dtype='int32')
#         seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
#         sentence_input = seq_index_layer([time_distributed_input, 0])
#         sentence_mask_input = seq_index_layer([time_distributed_input, 1])
#         sentence_input = layers.Reshape((maxlen,))(sentence_input)
#         sentence_mask_input = layers.Reshape((maxlen,))(sentence_mask_input)
#         embedded_sequences = layers.Embedding(class_num + 1, emb_size, input_length=maxlen, trainable=True, mask_zero=True)(sentence_input)
#         # lstm_word = layers.Bidirectional(layers.GRU(maxlen, return_sequences=True))(embedded_sequences)
#         attn_word = Attention(config)([embedded_sequences, sentence_mask_input, sentence_mask_input])
#         sentenceEncoder = Model(time_distributed_input, attn_word)
#
#     # def compute_output_shape(self, input_shape):
#     #     return (input_shape[0][0],input_shape[0][1])
#
#     def compute_mask(self, input, input_mask=None):
#         # need not to pass the mask to next layers
#         return None
#
#     def compute_output_shape(self, input_shape):
#         return input_shape[0], input_shape[-1]


def get_model(config, return_session=False,no_cross=False):
    activation = 'relu'
    maxlen = config['maxlen']
    class_num = config['class_num']
    batch_size = config['batchsize']
    # hidden_unit = config['lstm_hidden_units']
    emb_size = config['emb_size']

    user_size = config['user_size']
    cross_feature_num = config['cross_feature_num']
    user_feature_num = config['user_feature_num']
    user_feature_size = config['user_feature_size']
    output_unit = config['output_unit']
    seq_num = config['seq_num']
    # seq_feat_num = config['seq_feat_num']
    seq_max_sentences = config['seq_max_sentences']
    hidden_unit = config['hidden_unit']
    # seq_group_index = config['atrank_seq_group']
    # target_seq = config['atrank_target_seq']
    is_amp = config['is_amp']
    is_serving = config['is_serving']

    role_id_input = layers.Input(shape=(), dtype='int32', batch_size=batch_size)
    # seq_id_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32')
    # seq_time_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32')
    # seq_time_gaps_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32')
    seq_id_input = layers.Input(shape=(seq_max_sentences, maxlen, ), dtype='int32', batch_size=batch_size)
    seq_time_input = layers.Input(shape=(seq_max_sentences, maxlen,), dtype='int32', batch_size=batch_size)
    seq_time_gaps_input = layers.Input(shape=(seq_max_sentences, maxlen,), dtype='int32', batch_size=batch_size)
    if is_serving:
        cross_feature_indices_input = layers.Input(shape=(None, 2,), dtype='int64')
        cross_feature_values_input = layers.Input(shape=(None,), dtype='float32')
        cross_feature_indices = layers.Lambda(lambda x: tf.reshape(x, (-1, 2)))(cross_feature_indices_input)
        cross_feature_values = layers.Lambda(lambda x: tf.reshape(x, [-1]))(cross_feature_values_input)
        cross_feature_input = layers.Lambda(lambda x: tf.SparseTensor(indices=x[0], values=x[1], dense_shape=[tf.shape(seq_id_input)[0], cross_feature_num])) \
            ([cross_feature_indices, cross_feature_values])
    else:
        cross_feature_input = layers.Input(shape=(cross_feature_num,), dtype='float32', sparse=True, batch_size=batch_size)
    user_feature_input = layers.Input(shape=(user_feature_num,), dtype='int32', batch_size=batch_size)
    output_mask_input = layers.Input(shape=(output_unit,), dtype='float32', batch_size=batch_size)
    cur_time_input = layers.Input(shape=(), dtype='int32', batch_size=batch_size)

    seq_index_layer = layers.Lambda(lambda x: x[0][:,:, x[1]])
    seq_time = seq_index_layer([seq_time_input, 0])

    layers_emb_user_id = layers.Embedding(class_num , emb_size, input_length=maxlen, trainable=True, mask_zero=True)(seq_id_input)
    # emb_role_id = layers_emb_user_id(role_id_input)

    # time_distributed_inputs_tmp = list(map(layers.Reshape((seq_max_sentences, 1, maxlen,)), [seq_id_input,seq_time_input]))
    # time_distributed_inputs = layers.Concatenate(axis=2)(time_distributed_inputs_tmp)
    # print(seq_id_input.get_shape().as_list())
    print(layers_emb_user_id.get_shape().as_list())
    review_encoder = layers.TimeDistributed(Attention2(config))(layers_emb_user_id)
    # lstm_sentence = layers.Bidirectional(layers.GRU(maxlen, return_sequences=True))(review_encoder)
    print(seq_time.get_shape().as_list())
    seqs_embeddings = Attention(config)([review_encoder,seq_time,seq_time])
    # print(seqs_embeddings.get_shape().as_list())
    #
    # seqs_lstm = []
    # for i in range(seq_num):
    #     # seq_feat_num
    #     seq_i = seq_index_layer([seq_id_input, i])
    #     seq_i_embeddings = layers.Embedding(class_num, emb_size, mask_zero=True)(seq_i)
    #     seq_i_lstm = layers.LSTM(units=hidden_unit)(seq_i_embeddings)
    #     # seq_i_lstm = seq_index_layer([seq_i_embeddings, 0])
    #     seqs_lstm.append(seq_i_lstm)

    # seqs_embeddings = layers.Concatenate(axis=-1)(seqs_lstm) if len(seqs_lstm) > 1 else seqs_lstm[0]

    cross_feature = DenseLayerForSparse(cross_feature_num, hidden_unit, activation)(cross_feature_input)
    # cross_feature = layers.Lambda(lambda x: tf.ones([tf.shape(seq_id_input)[0], 128]))(1)

    layers_emb_fm1_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=1)
    layers_emb_fm2_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=emb_size)
    layers_FM = BiInteractionPooling()
    user_feature_1 = layers.Flatten()(layers_emb_fm1_user_feature(user_feature_input))
    user_feature_2 = layers.Flatten()(layers_FM(layers_emb_fm2_user_feature(user_feature_input)))
    user_feature = layers.Concatenate(axis=1)([user_feature_1, user_feature_2])

    if no_cross:
        all_feature = layers.Concatenate(axis=-1)([seqs_embeddings, user_feature])
    else:
        all_feature = layers.Concatenate(axis=-1)([seqs_embeddings, cross_feature, user_feature])

    # output = layers.Dense(output_unit, activation='softmax')(all_feature)

    output = layers.Dense(output_unit)(all_feature)
    if is_serving:
        output = tf.sigmoid(output)
    else:
        paddings = tf.ones_like(output) * (-2 ** 32 + 1)
        output = tf.where(tf.equal(output_mask_input, 0), paddings, output)
        output = tf.sigmoid(output)

    # output = tf.multiply(tf.exp(output), output_mask)
    # output = output / tf.reduce_sum(output, -1, True)
    # epsilon_ = _constant_to_tensor(epsilon(), output.dtype.base_dtype)
    # output = tf.clip_by_value(output, epsilon_, 1. - epsilon_)

    if is_serving:
        model = Model(inputs=[role_id_input, seq_id_input, seq_time_input, seq_time_gaps_input, cross_feature_indices_input, cross_feature_values_input,
                              user_feature_input, cur_time_input], outputs=[output])
    else:
        model = Model(inputs=[role_id_input, seq_id_input, seq_time_input, seq_time_gaps_input, cross_feature_input,
                              user_feature_input, output_mask_input, cur_time_input], outputs=[output])

    # for layer in model.layers:
    #     if hasattr(layer, 'kernel_regularizer'):
    #         layer.kernel_regularizer = regularizers.l2(0.000001)

    opt = tf.keras.optimizers.Adam()
    # opt = tf.keras.optimizers.SGD(0.1)
    if is_amp:
        opt = tf.train.experimental.enable_mixed_precision_graph_rewrite(opt)
    loss_dict = {'1': 'mean_squared_error', '2': 'binary_crossentropy'}
    # loss = zzn_loss
    loss = 'categorical_crossentropy'
    # loss = 'binary_crossentropy'
    model.compile(loss=loss_dict.get(str(output_unit), loss),
                  optimizer=opt,
                  metrics=['accuracy'])

    print('summary:')
    print(model.summary())
    sess = K.get_session()
    sess.run(tf.compat.v1.local_variables_initializer())
    sess.run(tf.compat.v1.global_variables_initializer())
    sess.run(tf.compat.v1.tables_initializer())

    if return_session:
        return model, sess
    else:
        return model
