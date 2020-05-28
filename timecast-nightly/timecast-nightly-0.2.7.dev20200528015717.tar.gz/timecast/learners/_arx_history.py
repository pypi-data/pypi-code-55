"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement strided histories
    * Figure out normalizing
"""
import warnings
from typing import Tuple
from typing import Union

import flax
import jax.numpy as jnp
import numpy as np

from timecast.learners._linear import Linear
from timecast.learners.base import NewMixin


default_output_shape: int = 1


class _ARXHistory(NewMixin, flax.nn.Module):
    """AR online learner helper"""

    def apply(
        self,
        data: np.ndarray,
        output_shape: Union[Tuple[int, ...], int] = default_output_shape,
        constrain: bool = True,
        name: str = "ARXHistory",
    ):
        """
        Args:
            data (np.ndarray): (batch, history_len, input_dim)
            output_shape (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            constrain: force one parameter per for each slot in history. TODO:
            explain this better
            name (str): name to pass to Linear

        Returns:
            np.ndarray: result
        """
        # TODO: Check shape of features and reshape if necessary
        input_shape = data.shape[2:]
        history_shape = data.shape[1:]

        # TODO (flax): We really shouldn't need state to just have some local
        # variables set in is_initializing...
        self.history_shape = self.state("history_shape", shape=(history_shape))
        if self.is_initializing():
            self.history_shape.value = history_shape
        else:
            if history_shape != self.history_shape.value:
                raise ValueError(
                    "Got input_shape {}, expected input_shape {}".format(
                        history_shape, self.history_shape.value
                    )
                )

        if jnp.isscalar(output_shape):
            output_shape = (output_shape,)

        if constrain:
            # If we have the non-default output_shape and it doesn't match input_shape
            if output_shape != default_output_shape and input_shape != output_shape:
                warnings.warn(
                    "When constrained, input data shape must equal output data"
                    "shape. Got input_shape {} and output_shape {}. Coercing"
                    "output_shape to input_shape".format(input_shape, output_shape)
                )
            output_shape = input_shape
            input_axes = (1,)
        else:
            input_axes = tuple(range(1, data.ndim))

        return Linear(
            inputs=data,
            output_shape=output_shape,
            input_axes=input_axes,
            batch_axes=(0,),
            bias=True,
            dtype=jnp.float32,
            kernel_init=flax.nn.initializers.zeros,
            bias_init=flax.nn.initializers.zeros,
            precision=None,
            name="Linear",
        )


class ARXHistory(NewMixin, flax.nn.Module):
    """AR online learner with history as input"""

    def apply(
        self,
        features: np.ndarray = None,
        targets: np.ndarray = None,
        output_shape: Union[Tuple[int, ...], int] = 1,
        constrain: bool = True,
    ):
        """
        Notation
            * x = features
            * y = targets
            * H = history_len

        Estimates the following:
        
            \hat{y} = \sum_{i = 1}^{H + 1} A_i x_{t - i - 1} + a
                      \sum_{i = 1} ^ H B_i y_{t - i} + b

        Notes:
            * Assumes `features` and `targets` have three dimensions: (batch,
            history, data). Any extra dimensions are part of the data shape
            * Doesn't care if features and targets have different history or
            input dimensions

        Args:
            features (np.ndarray): feature data
            targets (np.ndarray): target data
            output_shape (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            constrain: force one parameter per for each slot in history. TODO:
            explain this better

        Returns:
            np.ndarray: result
        """

        Ax, By = 0, 0

        self.has_features = self.state("has_features", shape=())
        self.has_targets = self.state("has_targets", shape=())

        has_features = features is not None and features.ndim > 0
        has_targets = targets is not None and targets.ndim > 0

        if self.is_initializing():
            if not has_features and not has_targets:
                raise ValueError("Need one or both of features and targets")
            self.has_features.value = has_features
            self.has_targets.value = has_targets
        else:
            if has_features and has_targets and features.shape[0] != targets.shape[0]:
                raise ValueError("Features and targets need to have same sized batch")
            if not has_features and self.has_features.value:
                raise ValueError("Expected features, but got None")
            if has_features and not self.has_features.value:
                raise ValueError("Did not expected features, but got features")
            if not has_targets and self.has_targets.value:
                raise ValueError("Expected targets, but got None")
            if has_targets and not self.has_targets.value:
                raise ValueError("Did not expected targets, but got targets")

        if has_features:
            Ax = _ARXHistory(
                data=features, output_shape=output_shape, constrain=constrain, name="Features"
            )

        if has_targets:
            By = _ARXHistory(
                data=targets, output_shape=output_shape, constrain=constrain, name="Targets"
            )

        return Ax + By
