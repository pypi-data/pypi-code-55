"""pt.py: utilities for pytorch."""

from argparse import Namespace, ArgumentParser
from typing import Any, Iterable, Mapping, Optional, Sequence, Type

import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler

from shinyutils.argp import ClassType, KeyValuePairsType, CommaSeparatedInts
from shinyutils.subcls import get_subclasses

__all__ = ["PTOpt", "FCNet"]


class PTOpt:

    """Wrapper around pytorch optimizer and learning rate scheduler."""

    def __init__(
        self,
        weights: Iterable[torch.Tensor],
        optim_cls: Type[Optimizer],
        optim_params: Mapping[str, Any],
        lr_sched_cls: Optional[Type[_LRScheduler]] = None,
        lr_sched_params: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self._optimizer = optim_cls(weights, **optim_params)
        if lr_sched_cls is not None:
            self._lr_sched = lr_sched_cls(self._optimizer, **lr_sched_params)
        else:
            self._lr_sched = None

    def zero_grad(self) -> None:
        self._optimizer.zero_grad()

    def step(self) -> None:
        self._lr_sched.step()
        self._optimizer.step()

    @classmethod
    def from_args(
        cls, weights: Iterable[torch.Tensor], args: Namespace, arg_prefix: str = ""
    ) -> "PTOpt":
        if arg_prefix:
            arg_prefix += "_"
        varargs = vars(args)
        if f"{arg_prefix}lr_sched_cls" not in varargs:
            varargs[f"{arg_prefix}lr_sched_cls"] = None
            varargs[f"{arg_prefix}lr_sched_params"] = None
        return cls(
            weights,
            varargs[f"{arg_prefix}optim_cls"],
            varargs[f"{arg_prefix}optim_params"],
            varargs[f"{arg_prefix}lr_sched_cls"],
            varargs[f"{arg_prefix}lr_sched_params"],
        )

    @staticmethod
    def add_parser_args(
        base_parser: ArgumentParser,
        arg_prefix: str = "",
        group_title: Optional[str] = None,
        default_optim_cls: Optional[Type[Optimizer]] = None,
        default_optim_params: Optional[Mapping[str, Any]] = None,
        add_lr_decay: bool = True,
        default_lr_decay_cls: Optional[Type[_LRScheduler]] = None,
        default_lr_decay_params: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Add options to the base parser for pytorch optimizer and lr decay."""
        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            f"--{arg_prefix}optim-cls",
            type=ClassType(Optimizer),
            choices=get_subclasses(Optimizer),
            required=default_optim_cls is None,
            default=default_optim_cls,
        )

        if default_optim_params is None:
            default_optim_params = dict()
        base_parser.add_argument(
            f"--{arg_prefix}optim-params",
            type=KeyValuePairsType(),
            default=default_optim_params,
        )

        if not add_lr_decay:
            return

        base_parser.add_argument(
            f"--{arg_prefix}lr-decay-cls",
            type=ClassType(_LRScheduler),
            required=default_lr_decay_cls is None,
            default=default_lr_decay_cls,
        )

        if default_lr_decay_params is None:
            default_lr_decay_params = dict()
        base_parser.add_argument(
            f"--{arg_prefix}lr-decay-params",
            type=KeyValuePairsType(),
            default=default_lr_decay_params,
        )


class FCNet(nn.Module):

    """Template for a fully connected network."""

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        hidden_sizes: Sequence[int],
        hidden_act=nn.ReLU,
        out_act=None,
    ) -> None:
        super().__init__()
        layer_sizes = [in_dim] + hidden_sizes + [out_dim]
        self.layers = nn.ModuleList(
            [nn.Linear(ls, ls_n) for ls, ls_n in zip(layer_sizes, layer_sizes[1:])]
        )
        self.hidden_act = hidden_act
        self.out_act = out_act

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = self.hidden_act(layer(x))
        x = self.layers[-1](x)
        if self.out_act is not None:
            x = self.out_act(x)
        return x

    @classmethod
    def from_args(cls, args, arg_prefix=""):
        if arg_prefix:
            arg_prefix += "_"
        varargs = vars(args)
        return cls(
            varargs[f"{arg_prefix}fcnet_indim"],
            varargs[f"{arg_prefix}fcnet_outdim"],
            varargs[f"{arg_prefix}fcnet_hidden_sizes"],
        )

    @staticmethod
    def add_parser_args(
        base_parser,
        arg_prefix="",
        group_title=None,
        default_indim=None,
        default_outdim=None,
        default_hidden_sizes=None,
    ):
        """Add options to base_parser for building a FCNet object."""
        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            f"--{arg_prefix}fcnet-indim",
            type=int,
            required=default_indim is None,
            default=default_indim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-outdim",
            type=int,
            required=default_outdim is None,
            default=default_outdim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-hidden-sizes",
            type=CommaSeparatedInts(),
            required=default_hidden_sizes is None,
            default=default_hidden_sizes,
        )
