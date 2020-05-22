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
        if len(self.embedding_output_layer) > 1:
            k_out = tf.keras.layers.concatenate(self.embedding_output_layer, axis=1)  # emebedding 维度变多
        else:
            k_out = self.embedding_output_layer[0]

        fm_out = self.fm(k_out)

        dnn_out = self.dnn(k_out)
        dnn_out = tf.keras.layers.Dense(1, use_bias=False, activation=None)(dnn_out)

        # 合并输出
        out = tf.keras.layers.add([self.linear_output_layer, fm_out, dnn_out])
        out = self.prediction_output_layer(out)

        model = tf.keras.models.Model(inputs=self.inputs, outputs=out)
        return model


if __name__ == '__main__':
    fcs = [NumericColumn('num'), CategoricalColumn('cat')]

    print(DeepFM(fcs).summary())
