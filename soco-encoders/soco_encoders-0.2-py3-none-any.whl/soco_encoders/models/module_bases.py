# @Time    : 9/20/17 2:10 PM
# @Author  : Tiancheng Zhao
import torch.nn as nn


class BaseEncoder(nn.Module):
    DEFAULT = "default"
    ANSWER = "answer"
    TSCORE = "tscore"

    def __init__(self, vocab, config):
        super(BaseEncoder, self).__init__()
        self.vocab = vocab
        self.config = config
        self.use_gpu = config.use_gpu

    def encode(self, *args, **kwargs):
        raise NotImplementedError

    def tokenize_to_ids(self, sent):
        raise NotImplementedError

    def tokenize_to_pieces(self, sent):
        raise NotImplementedError

    def advanced_encode(self, *args, **kwargs):
        pass

    def get_embedding_dimension(self):
        raise NotImplementedError
