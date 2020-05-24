import torch
import torch.nn as nn
from timm.models.layers import Swish


class BatchNorm2dAct(nn.BatchNorm2d):
    def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True, act_layer=None):
        super(BatchNorm2dAct, self).__init__(
            num_features, eps=eps, momentum=momentum, affine=affine, track_running_stats=track_running_stats)
        if act_layer is not None:
            self.act = act_layer(inplace=True)
        else:
            self.act = None

    def forward(self, x):
        x = self.forward(x)
        if self.act is not None:
            x = self.act(x)
        return x


class BatchNorm2dReLU(nn.BatchNorm2d):
    def __init__(self, num_features, nonnlin=True, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True):
        super(BatchNorm2dReLU, self).__init__(
            num_features, eps=eps, momentum=momentum, affine=affine, track_running_stats=track_running_stats)
        if nonnlin:
            self.act = nn.ReLU(inplace=True)
        else:
            self.act = None

    def forward(self, x):
        x = self.forward(x)
        if self.act is not None:
            x = self.act(x)
        return x


class BatchNorm2dSwish(nn.BatchNorm2d):
    def __init__(self, num_features, nonnlin=True, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True):
        super(BatchNorm2dSwish, self).__init__(
            num_features, eps=eps, momentum=momentum, affine=affine, track_running_stats=track_running_stats)
        if nonnlin:
            self.act = Swish()
        else:
            self.act = None

    def forward(self, x):
        x = self.forward(x)
        if self.act is not None:
            x = self.act(x)
        return x


def instance_std(x, eps=1e-5):
    B, C, H, W = x.shape
    x = x.reshape(B * C, 1, -1)
    return torch.sqrt(x.var(dim=-1, unbiased=False, keepdim=True) + eps).reshape(B, C, 1, 1)


def group_std(x, groups, eps=1e-5):
    B, C, H, W = x.shape
    x = x.reshape(B, groups, -1)
    x = x / torch.sqrt(x.var(dim=-1, unbiased=False, keepdim=True).reshape(B, groups, -1) + eps)
    return x.reshape(B, C, H, W)


class EvoNormB02d(nn.Module):
    def __init__(self, num_features, nonlin=True, eps=1e-5, momentum=0.1):
        super(EvoNormB02d, self).__init__()
        self.nonlin = nonlin
        self.eps = eps
        self.momentum = momentum
        param_shape = (1, num_features, 1, 1)
        self.weight = nn.Parameter(torch.ones(param_shape), requires_grad=True)
        self.bias = nn.Parameter(torch.zeros(param_shape), requires_grad=True)
        if nonlin:
            self.v = nn.Parameter(torch.ones(param_shape), requires_grad=True)
        self.register_buffer('running_var', torch.ones(1, num_features, 1, 1))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.ones_(self.weight)
        nn.init.zeros_(self.bias)
        if self.nonlin:
            nn.init.ones_(self.v)

    def forward(self, x):
        C = x.shape[1]
        if self.training:
            x = x.permute(1, 0, 2, 3).reshape(C, -1)
            var = x.var(dim=1, unbiased=True).reshape(1, C, 1, 1)
            self.running_var.copy_(self.momentum * var + (1 - self.momentum) * self.running_var)
        else:
            var = self.running_var
        if self.nonlin:
            x = x / torch.max(torch.sqrt(var + self.eps), self.v * x + instance_std(x, self.eps))
        return x * self.weight + self.bias


class EvoNormS02d(nn.Module):
    def __init__(self, num_features, nonlin=True, groups=8, eps=1e-5):
        super(EvoNormS02d, self).__init__()
        self.nonlin = nonlin
        self.groups = groups
        self.eps = eps
        param_shape = (1, num_features, 1, 1)
        self.weight = nn.Parameter(torch.ones(param_shape), requires_grad=True)
        self.bias = nn.Parameter(torch.zeros(param_shape), requires_grad=True)
        if nonlin:
            self.v = nn.Parameter(torch.ones(param_shape), requires_grad=True)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.ones_(self.weight)
        nn.init.zeros_(self.bias)
        if self.nonlinear:
            nn.init.ones_(self.v)

    def forward(self, x):
        if self.nonlinear:
            x = torch.sigmoid(self.v * x) * group_std(x, self.groups, self.eps)
        return x * self.weight + self.bias
