import torch as th
from torch import Tensor as Tensor
from typing import List


class Wrapper:
    def __init__(self, *gpu):
        self._gpu = list(gpu)
        if len(gpu) == 0:
            self.device = th.device("cpu")
        elif len(gpu) == 1:
            self.device = th.device("gpu")

    def variable(self, ldata: List) -> Tensor:
        """

        Args:
            ldata: list of data

        Returns:
            torch.Tensor
        """
        return th.tensor(ldata, requires_grad=True).to(self.device)

    def tensor(self, ldata: List) -> Tensor:
        """
        Grad disable tensor

        :param ldata:list type data

        :return: torch.tensor
        """
        return th.tensor(ldata, requires_grad=False).to(self.device)

