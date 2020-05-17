import torch
from torch import autograd
import numpy as np


def to_scalar(var):
    """
    返回 python 浮点数 (float)
    """
    return var.view(-1).data.tolist()[0]


def argmax(vec):
    """
    以 python 整数的形式返回 argmax
    Args:
        vec:

    Returns:

    """
    _, idx = torch.max(vec, 1)
    return to_scalar(idx)


def log_sum_exp(vec):
    """
    使用数值上稳定的方法为前向算法计算指数和的对数
    Args:
        vec: PyTorch Tensor type vector

    Returns:

    """
    max_score = vec[0, argmax(vec)]
    max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])
    return max_score + \
           torch.log(torch.sum(torch.exp(vec - max_score_broadcast)))
