#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : inn.
# @File         : BaseModel
# @Time         : 2020/5/19 2:24 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

from collections import namedtuple, OrderedDict

from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

import tensorflow as tf

from ..features.fc import Column
from ..features.fc import utils as fc_utils

from inn.layers import DNN, Prediction
from ..layers.interaction import FM

from ..layers.utils import get_activation_by_num_class


class BaseModel(object):

    def __init__(self,
                 fcs: List[Column] = None,
                 fm=FM(),
                 dnn=DNN(),
                 num_class=2,
                 dense_dim=1,
                 dense_activation=None,
                 early_stopping_epochs=3,
                 model_name='BaseModel'):
        self.fcs = fcs
        self.fc2input = list(fc_utils.get_fc2input_map(fcs))
        self.inputs = [v for k, v in self.fc2input]

        self.num_class = num_class
        self.activation = get_activation_by_num_class(num_class)

        self.dense_dim = dense_dim

        self.early_stopping_epochs = early_stopping_epochs
        self.model_name = model_name

        #################################
        self.fm = fm
        self.dnn = dnn
        # 线性部分
        self.linear_output_layer = fc_utils.get_linear_output(self.fc2input, dense_dim=1, dense_activation=None)

        # 高阶部分
        self.dense_output_layer = fc_utils.get_dense_out(self.fc2input, dense_dim=self.dense_dim,
                                                         dense_activation=dense_activation)
        self.embedding_output_layer = fc_utils.get_embedding_out(self.fc2input, embedding_dim='auto')

        self.prediction_output_layer = Prediction(num_class)

        self.model = self._build_model()

    @abstractmethod
    def _build_model(self):
        raise NotImplementedError()

    def fit(self, *args, **kwargs):
        return self.model.fit(*args, **kwargs)

    def predict(self, X):
        return self.model.predict(X)

    def summary(self, return_summary=True, to_file='model.png',
                show_shapes=True,
                rankdir='TB',
                dpi=96):
        if return_summary:
            self.model.summary()

        tf.keras.utils.plot_model(self.model, to_file=to_file,
                                  show_shapes=show_shapes,
                                  rankdir=rankdir,
                                  dpi=dpi)

    def compile(self,
                optimizer='rmsprop',
                loss=None,
                metrics=None,
                loss_weights=None,
                sample_weight_mode=None,
                weighted_metrics=None):
        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=metrics,
                           loss_weights=loss_weights,
                           sample_weight_mode=sample_weight_mode,
                           weighted_metrics=weighted_metrics)

    def callbacks(self):
        callbacks_list = [
            tf.keras.callbacks.ReduceLROnPlateau(factor=0.9, patience=2, verbose=1, min_lr=0.0001),
            # annealer = LearningRateScheduler(lambda x: min(0.01 * 0.9 ** x, 0.001), verbose=1)

            tf.keras.callbacks.ModelCheckpoint("filepath",
                                               monitor='val_loss',
                                               verbose=0,
                                               save_best_only=True,
                                               save_weights_only=False,
                                               mode='auto',
                                               save_freq='epoch'),

            tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                             min_delta=0,
                                             patience=self.early_stopping_epochs,
                                             verbose=0,
                                             mode='auto',
                                             baseline=None,
                                             restore_best_weights=False)
        ]
        return callbacks_list

    # todo: 学习率clr_callback, WandbCallback
