"""flax.nn.Module for predicting last value

Todo:
    * Implement last value n steps ago (requires state)
"""
import flax
import jax
import numpy as np

from timecast.learners.base import NewMixin


class PredictLast(NewMixin, flax.nn.Module):
    """Identity online learner"""

    def apply(self, x: np.ndarray):
        """
        Note:
            * Returns `x` as the prediction for the next time step

        Args:
            x (np.ndarray): input data

        Returns:
            np.ndarray: result
        """
        # TODO (flax): Remove this once flax updates
        _ = self.param("dummy", (), jax.nn.initializers.zeros)
        return x
