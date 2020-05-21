import torch
import torch.nn.functional as F
from torch import Tensor
from torch import distributions as dist
from torch import nn

from .base import BayesianBaseLayer


class BayesianLinear(BayesianBaseLayer):
    def __init__(self, n_in: int, n_out: int, bias: bool = True) -> None:
        super().__init__()
        self.n_in = n_in
        self.n_out = n_out
        self.bias = True

        self.weights_mu = nn.Parameter(
            torch.randn(n_out, n_in + bias) / 10, True
        )
        self.weights_rho = nn.Parameter(
            torch.randn(n_out, n_in + bias) / 10 - 3, True
        )
        self.epsilon = torch.zeros(n_out, n_in + bias)

    def sample_parameters(self) -> None:
        self.epsilon = torch.randn_like(self.epsilon)

    def set_to_best_prediction(self) -> None:
        self.epsilon = torch.zeros_like(self.epsilon)

    def forward(self, inputs: Tensor) -> Tensor:  # type: ignore
        if self.bias:
            inputs = torch.cat(
                (torch.ones(*inputs.shape[:-1], 1), inputs), dim=-1
            )

        return F.linear(inputs, self.weights)

    @property
    def weights(self) -> Tensor:
        return (
            self.weights_mu
            + torch.log(1 + torch.exp(self.weights_rho)) * self.epsilon
        )

    @property
    def kl_loss(self) -> Tensor:
        posterior = dist.Normal(
            loc=self.weights_mu,
            scale=torch.log(1 + torch.exp(self.weights_rho)),
        )
        prior = dist.Normal(
            loc=torch.zeros_like(self.weights_mu),
            scale=torch.ones_like(self.weights_rho),
        )

        return (
            posterior.log_prob(self.weights) - prior.log_prob(self.weights)
        ).mean()
