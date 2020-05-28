"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement batching
"""
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as np

from timecast.learners._arx_history import ARXHistory
from timecast.learners.base import NewMixin


def _none_init(rng, shape):
    """Initialize with scalar None"""
    return None


class ARX(NewMixin, flax.nn.Module):
    """AR online learner"""

    def apply(
        self,
        features: np.ndarray = None,
        targets: np.ndarray = None,
        history_len: int = 1,
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
            * Assumes `features` and `targets` are the shape of one time step
            of data
            * Delegates much of the error checking to ARXHistory

        Args:
            features (np.ndarray): feature data
            targets (np.ndarray): target data
            output_shape (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            history_len (int): length of history
            constrain: force one parameter per for each slot in history. TODO:
            explain this better

        Returns:
            np.ndarray: result
        """

        # TODO: Check and reshape inputs; for now assumes data is time x
        # dimension

        if history_len < 1:
            raise ValueError("Features require a history length of at least 1")

        has_features = features is not None and features.ndim > 0
        has_targets = targets is not None and targets.ndim > 0

        self.T = self.state("T", shape=())
        self.feature_history = self.state("feature_history", shape=(), initializer=_none_init)
        self.target_history = self.state("target_history", shape=(), initializer=_none_init)

        if self.is_initializing():
            self.T.value = 0

            if has_features:
                feature_history_shape = (history_len, features.shape[1])
                self.feature_history.value = jnp.zeros(feature_history_shape)
            if has_targets:
                target_history_shape = (history_len, targets.shape[1])
                self.target_history.value = jnp.zeros(target_history_shape)
        else:
            if has_features:
                self.feature_history.value = jnp.concatenate(
                    (self.feature_history.value, features)
                )[features.shape[0] :]

        feature_history = None if features is None else self.feature_history.value[None, :]
        target_history = None if targets is None else self.target_history.value[None, :]

        y_hat = ARXHistory(
            features=feature_history,
            targets=target_history,
            output_shape=output_shape,
            constrain=constrain,
        )

        if not self.is_initializing():
            # Update target history with data _after_ we have made calculations
            if has_targets:
                self.target_history.value = jnp.vstack((self.target_history.value, targets))[
                    targets.shape[0] :
                ]

            self.T.value += 1

        # If we have targets, then we need to wait one additional time step to
        # have a full target window
        if self.T.value + (1 if has_targets else 0) >= history_len:
            return y_hat
        else:
            return jax.lax.stop_gradient(y_hat)
