from typing import List, Optional, Tuple, Type

import torch
from torch import Tensor, jit

from ..base import BayesianBaseLayer


class BayesianBaseRnnCell(jit.ScriptModule, BayesianBaseLayer):
    def __init__(self, n_in: int, n_out: int, bias: bool = True) -> None:
        super().__init__()
        self.n_in = n_in
        self.n_out = n_out
        self.bias = bias

    def sample_parameters(self) -> None:
        raise NotImplementedError()

    def set_to_best_prediction(self) -> None:
        raise NotImplementedError()

    def init_state(self, batch_size: int) -> List[Tensor]:
        raise NotImplementedError()

    @jit.script_method
    def forward(
        self, inputs: Tensor, state: List[Tensor]
    ) -> Tuple[Tensor, List[Tensor]]:
        raise NotImplementedError()  # pragma: no cover

    @property
    def weights(self) -> Tensor:
        raise NotImplementedError()

    @property
    def kl_loss(self) -> Tensor:
        raise NotImplementedError()


class BayesianBaseRnn(jit.ScriptModule, BayesianBaseLayer):
    def __init__(
        self,
        n_in: int,
        n_out: int,
        cell: Type[BayesianBaseRnnCell],
        bias: bool = True,
    ) -> None:
        super().__init__()
        self.n_in = n_in
        self.n_out = n_out
        self.bias = bias
        self.cell = cell(n_in, n_out, bias)

    def sample_parameters(self) -> None:
        self.cell.sample_parameters()

    def set_to_best_prediction(self) -> None:
        self.cell.set_to_best_prediction()

    def init_state(self, batch_size: int) -> List[Tensor]:
        return self.cell.init_state(batch_size)

    @jit.script_method
    def forward(
        self, inputs: Tensor, state: Optional[List[Tensor]] = None
    ) -> Tuple[Tensor, List[Tensor]]:  # pragma: no cover
        state_ = self.init_state(inputs.shape[0]) if state is None else state
        outputs: List[Tensor] = []
        for inputs_ in inputs.unbind(1):
            outputs_, state_ = self.cell(inputs_, state_)
            outputs += [outputs_]
        return torch.stack(outputs, 1), state_

    @property
    def weights(self) -> Tensor:
        return self.cell.weights

    @property
    def kl_loss(self) -> Tensor:
        return self.cell.kl_loss
