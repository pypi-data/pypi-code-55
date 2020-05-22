#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : inn.
# @File         : DeepFM
# @Time         : 2020/5/22 10:03 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from collections import OrderedDict

from inn.models.BaseModel import BaseModel

import tensorflow as tf
from inn.features.fc import *

from inn.layers import DNN
from inn.layers.interaction import FM


class DeepFM(BaseModel):

    def __init__(self, fcs: List[Column],
                 fm=FM(),
                 dnn=DNN(),
                 num_class=2,
                 model_name='DeepFM',
                 **kwargs):
        super().__init__(fcs=fcs,
                         fm=fm,
                         dnn=dnn,
                         num_class=num_class,
                         model_name=model_name,
                         **kwargs)

    def _build_model(self, **kwargs):
        """
        sigmoid(fm, dnn)
        """

        if self.dense_output_layer:
            k_out = tf.keras.layers.concatenate([self.embedding_output_layer, self.dense_output_layer])
        else:
            k_out = self.embedding_output_layer

        fm_out = self.fm(k_out)
        fm_out = tf.keras.layers.add([self.linear_output_layer, fm_out])

        dnn_out = self.dnn(k_out)

        out = tf.keras.layers.concatenate([fm_out, dnn_out])
        out = self.prediction_output_layer()(out)

        tf.keras.models.Model(inputs=self.inputs, outputs=out)

        self.compile()
