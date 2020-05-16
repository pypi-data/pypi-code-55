import torch
from torch import nn
import torch.nn.functional as F


class VirtualBatchNorm(nn.Module):
    def __init__(self, num_features, eps=1e-5):
        super(VirtualBatchNorm, self).__init__()
        self.num_features = num_features
        self.eps = eps
        self.mean = None
        self.var = None
        self.weight = nn.parameter.Parameter(torch.Tensor(num_features))
        self.bias = nn.parameter.Parameter(torch.Tensor(num_features))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.ones_(self.weight)
        nn.init.zeros_(self.bias)

    def forward(self, x):
        if self.mean is None and self.var is None:
            self.mean = torch.mean(x, dim=[1,2], keepdim=True)
            self.var = torch.var(x, dim=[1,2], keepdim=True)
            return F.batch_norm(
                x, self.mean, self.var, self.weight, self.bias, eps=self.eps)
        else:
            return F.batch_norm(
                x, self.mean, self.var, self.weight, self.bias, eps=self.eps)
            self.mean = None
            self.var = None
