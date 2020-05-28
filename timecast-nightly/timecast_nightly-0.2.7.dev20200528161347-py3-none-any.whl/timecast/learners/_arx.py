"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement batching
    * Implement projections
"""
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as np

from timecast.learners._arx_history import ARXHistory
from timecast.learners.base import NewMixin
from timecast.utils.ar import historify


def _none_init(rng, shape):
    """Initialize with scalar None"""
    return None


class ARX(NewMixin, flax.nn.Module):
    """AR online learner"""

    def apply(
        self,
        targets: np.ndarray = None,
        features: np.ndarray = None,
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
        
            \hat{y} = \sum_{i = 1}^{H + 1} B_i x_{t - i - 1} + a
                      \sum_{i = 1} ^ H A_i y_{t - i} + b

        Notes:
            * Assumes `features` and `targets` are the shape of one time step
            of data
            * Delegates much of the error checking to ARXHistory

        Args:
            targets (np.ndarray): target data
            features (np.ndarray): feature data
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

        has_targets = targets is not None and targets.ndim > 0
        has_features = features is not None and features.ndim > 0

        self.T = self.state("T", shape=())
        self.target_history = self.state("target_history", shape=(), initializer=_none_init)
        self.feature_history = self.state("feature_history", shape=(), initializer=_none_init)

        if self.is_initializing():
            self.T.value = 0

            if has_targets:
                target_history_shape = (history_len, targets.shape[1])
                self.target_history.value = jnp.zeros(target_history_shape)
            if has_features:
                feature_history_shape = (history_len, features.shape[1])
                self.feature_history.value = jnp.zeros(feature_history_shape)

        target_histories, feature_histories = None, None
        if has_targets:
            target_histories = historify(
                jnp.vstack((self.target_history.value, targets))[:-1], history_len=history_len
            )

        if has_features:
            feature_histories = historify(
                jnp.vstack((self.feature_history.value, features))[1:], history_len=history_len
            )

        print(target_histories.shape, feature_histories.shape)

        y_hat = ARXHistory(
            targets=target_histories,
            features=feature_histories,
            output_shape=output_shape,
            constrain=constrain,
        )

        # TODO: Don't duplicate the vstacks (modulo index difference for target_history)
        if not self.is_initializing():
            # Update target history with data _after_ we have made calculations
            if has_targets:
                self.target_history.value = jnp.vstack((self.target_history.value, targets))[
                    targets.shape[0] :
                ]
            if has_features:
                self.feature_history.value = jnp.vstack((self.feature_history.value, features))[
                    features.shape[0] :
                ]

            self.T.value += 1

        print(self.T.value)
        print(self.target_history.value)
        print(self.feature_history.value)

        # If we have targets, then we need to wait one additional time step to
        # have a full target window
        if self.T.value + (1 if has_targets else 0) >= history_len:
            return y_hat
        else:
            return jax.lax.stop_gradient(y_hat)
