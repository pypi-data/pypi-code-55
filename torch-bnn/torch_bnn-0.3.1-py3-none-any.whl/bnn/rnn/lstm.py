from typing import List, Tuple

import torch
import torch.nn.functional as F
from torch import Tensor
from torch import distributions as dist
from torch import jit, nn

from .base import BayesianBaseRnn, BayesianBaseRnnCell


class BayesianLstmCell(BayesianBaseRnnCell):
    def __init__(self, n_in: int, n_out: int, bias: bool = True) -> None:
        super().__init__(n_in, n_out, bias)

        self.weights_mu = nn.Parameter(
            torch.randn(4 * n_out, n_in + n_out + bias) / 10, True
        )
        self.weights_rho = nn.Parameter(
            torch.randn(4 * n_out, n_in + n_out + bias) / 10 - 5, True
        )
        self.epsilon = torch.zeros(4 * n_out, n_in + n_out + bias)

    def _weights(self) -> Tensor:
        """
        Method created to work with jit.

        Returns
        -------
        Tensor
            Weights of shape n_out X n_in + n_out ( + 1 if bias )
        """
        return (
            self.weights_mu
            + torch.log(1 + torch.exp(self.weights_rho)) * self.epsilon
        )

    def sample_parameters(self) -> None:
        self.epsilon = torch.rand_like(self.epsilon)

    def set_to_best_prediction(self) -> None:
        self.epsilon = torch.zeros_like(self.epsilon)

    def init_state(self, batch_size: int) -> List[Tensor]:
        return [
            torch.zeros(batch_size, self.n_out),
            torch.zeros(batch_size, self.n_out),
        ]

    @jit.script_method
    def forward(
        self, inputs: Tensor, state: List[Tensor]
    ) -> Tuple[Tensor, List[Tensor]]:  # pragma: no cover
        if self.bias:
            inputs = torch.cat(
                (torch.ones(inputs.shape[0], 1), inputs, state[0]), dim=1,
            )
        else:
            inputs = torch.cat((inputs, state[0]), dim=-1)

        gates = torch.sigmoid(F.linear(inputs, self._weights()))
        i, g, f, o = torch.chunk(gates, 4, dim=1)
        long_memory = f * state[1] + i * g
        state_ = [o * long_memory, long_memory]

        return state_[0], state_

    @property
    def weights(self) -> Tensor:
        return self._weights()

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


class BayesianLstm(BayesianBaseRnn):
    def __init__(self, n_in: int, n_out: int, bias: bool = True) -> None:
        super().__init__(n_in, n_out, BayesianLstmCell, bias)
