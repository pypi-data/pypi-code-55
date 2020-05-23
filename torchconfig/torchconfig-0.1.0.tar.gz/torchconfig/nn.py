import torch.nn as nn

from torchconfig.filter import filter_args


# Activation Layers
NAME_TO_NN_ACTIVATIONS = {
    "ELU": nn.ELU,
    "Hardshrink": nn.Hardshrink,
    "Hardtanh": nn.Hardtanh,
    "LeakyReLU": nn.LeakyReLU,
    "LogSigmoid": nn.LogSigmoid,
    "MultiheadAttention": nn.MultiheadAttention,
    "PReLU": nn.PReLU,
    "ReLU": nn.ReLU,
    "ReLU6": nn.ReLU6,
    "RReLU": nn.RReLU,
    "SELU": nn.SELU,
    "CELU": nn.CELU,
    "GELU": nn.GELU,
    "Sigmoid": nn.Sigmoid,
    "Softplus": nn.Softplus,
    "Softshrink": nn.Softshrink,
    "Softsign": nn.Softsign,
    "Tanh": nn.Tanh,
    "Tanhshrink": nn.Tanhshrink,
    "Threshold": nn.Threshold,
    "Softmin": nn.Softmin,
    "Softmax": nn.Softmax,
    "Softmax2d": nn.Softmax2d,
    "LogSoftmax": nn.LogSoftmax,
    "AdaptiveLogSoftmaxWithLoss": nn.AdaptiveLogSoftmaxWithLoss,
}


def get_activation_layer_from_args(*args, **kwargs):
    func = NAME_TO_NN_ACTIVATIONS[kwargs["name"]]
    return func(*args, **filter_args(kwargs, func))


def get_activation_layer_from_dict(in_dict):
    return get_activation_layer_from_args(**in_dict)
