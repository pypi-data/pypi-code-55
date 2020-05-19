import torch
from torch import Tensor
from torch import nn
from typing import Union, Tuple, List, Iterable, Dict
from collections import OrderedDict
import os
import json


class MLP(nn.Module):
    """Performs MLP
    """

    def __init__(self,
                 word_embedding_dimension: int,
                 output_dimension: int,
                 num_layer: int = 2,
                 dropout: float=0.1,
                 linear_output=False
                 ):
        super(MLP, self).__init__()

        self.config_keys = ['word_embedding_dimension', 'output_dimension', 'num_layer', 'dropout', 'linear_output']

        self.word_embedding_dimension = word_embedding_dimension
        self.output_dimension = output_dimension
        self.num_layer = num_layer
        self.dropout = dropout
        self.linear_output = linear_output
        layers = OrderedDict()
        for i in range(num_layer):
            if i == 0:
                layers['fc-0'] = nn.Linear(word_embedding_dimension, output_dimension)
                layers['act-0'.format(i)] = nn.Tanh()
            else:
                layers['dropout-{}'.format(i)] = nn.Dropout(0.1)
                layers['fc-{}'.format(i)] = nn.Linear(output_dimension, output_dimension)
                layers['act-{}'.format(i)] = nn.Tanh()
        if linear_output:
            layers.pop('act-{}'.format(num_layer-1))

        print(layers)
        self.mlp = nn.Sequential(layers)

    def forward(self, features: Dict[str, Tensor]):
        sentence_embedding = features['sentence_embedding']
        new_sentence_embedding = self.mlp(sentence_embedding)
        features.update({'sentence_embedding': new_sentence_embedding})
        return features

    def get_sentence_embedding_dimension(self):
        return self.output_dimension

    def get_config_dict(self):
        return {key: self.__dict__[key] for key in self.config_keys}

    def save(self, output_path):
        with open(os.path.join(output_path, 'config.json'), 'w') as fOut:
            json.dump(self.get_config_dict(), fOut, indent=2)

        torch.save(self.state_dict(), os.path.join(output_path, 'pytorch_model.bin'))


    @staticmethod
    def load(input_path):
        with open(os.path.join(input_path, 'config.json')) as fIn:
            config = json.load(fIn)

        weights = torch.load(os.path.join(input_path, 'pytorch_model.bin'))
        model = MLP(**config)
        model.load_state_dict(weights)
        return model
