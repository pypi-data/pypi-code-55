"""flax.nn.Module for a principal component regression online learner."""
from typing import Any
from typing import Iterable
from typing import Tuple
from typing import Union

import flax
import jax.numpy as jnp
import numpy as np

from timecast.learners._linear import Linear
from timecast.learners.base import FitMixin
from timecast.learners.base import NewMixin
from timecast.utils import random
from timecast.utils.ar import compute_gram
from timecast.utils.ar import fit_gram
from timecast.utils.pcr import compute_projection


class PCR(NewMixin, FitMixin, flax.nn.Module):
    """PCR online learner"""

    def apply(
        self,
        x: np.ndarray,
        history_len: int,
        projection: np.ndarray,
        output_dim: Union[Tuple[int, ...], int] = 1,
        history: np.ndarray = None,
        loc: Union[np.ndarray, float] = None,
        scale: Union[np.ndarray, float] = None,
    ):
        """
        Todo:
            * AR doesn't take any history
        output_dim (Union[Tuple[int, ...], int]): int or tuple describing
        output shape

        Note:
            * We expect that `x` is one- or two-dimensional
            * We reshape `x` to ensure its first axis is time and its second
              axis is input_features

        Args:
            x (np.ndarray): input data
            history_len (int): length of AR history length
            output_dim (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            history (np.ndarray, optional): Defaults to None. Optional
            initialization for history
            loc: mean for centering data
            scale: std for normalizing data

        Returns:
            np.ndarray: result
        """
        if jnp.isscalar(x):
            x = jnp.array([[x]])
        if x.ndim == 1:
            x = x.reshape(1, -1)

        self.history = self.state(
            "history", shape=(history_len, x.shape[1]), initializer=flax.nn.initializers.zeros
        )

        if self.is_initializing() and history is not None:
            self.history.value = jnp.vstack((self.history.value, history))[history.shape[0] :]
        elif not self.is_initializing():
            self.history.value = jnp.vstack((self.history.value, x))[x.shape[0] :]

        inputs = self.history.value.reshape(1, -1)

        if loc is not None:
            inputs -= loc

        if scale is not None:
            inputs /= scale

        inputs @= projection

        y = Linear(
            inputs=inputs,
            output_shape=output_dim,
            input_axes=(0, 1),
            bias=True,
            dtype=jnp.float32,
            kernel_init=flax.nn.initializers.zeros,
            bias_init=flax.nn.initializers.zeros,
            precision=None,
            name="Linear",
        )
        return y

    @classmethod
    def fit(
        cls,
        data: Iterable[Tuple[np.ndarray, np.ndarray, Any]],
        input_dim: int,
        history_len: int,
        output_dim: int = 1,
        k: int = None,
        normalize: bool = True,
        alpha: float = 1.0,
        key: jnp.ndarray = None,
        history: np.ndarray = None,
        name: str = "PCR",
        **kwargs
    ) -> flax.nn.Model:
        """Receives data as an iterable of tuples containing input time series,
        true time series

        Todo:
            * We assume input_dim is one-dimensional; we should flatten if not
            * Really intended for passing in timeseries at a time, not
            individual time series observations; is this the right general API?
            * Shape is (1, input_dim); what about mini-batches?

        Notes:
            * Use (1, history_len * input_dim) vectors as features (could
            consider other representations)
            * Ignore true value (i.e., look at features only) (should we
            consider impact of features on dependent variable?)
            * Given a time series of length N and a history of length H,
            construct N - H + 1 windows
            * We could infer input_dim from data, but for now, require
            users to explicitly provide
            * Assumes we get tuples of time series, not individual time series
            observations

        Args:
            data: an iterable of tuples containing input/truth pairs of time
            series plus any auxiliary value
            input_dim: number of feature dimensions in input
            history_len: length of history to consider
            output_dim: number of feature dimensions in output
            k: number of PCA components to keep. Default is min(num_histories,
            normalize: zscore data or not
            input_dim)
            alpha: Parameter to pass to ridge regression for AR fit
            key: random key for jax random
            history: Any history to pass to AR
            name: name for the top-level module
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        XTX, XTY = compute_gram(data, input_dim, output_dim, history_len)
        num_features = input_dim * history_len

        # Compute k
        min_dim = min(num_features, XTX.observations)
        k = min_dim if k is None else min(k, min_dim)

        projection = compute_projection(XTX.matrix(normalize=normalize), k)

        # X: (n, d)
        # XTX.matrix: (d, d)
        # projection: (d, k)
        # X @ projection: (n, k)
        # (X @ projection).T @ (X @ projection): (k, k)
        # projection.T @ X.T @ X @ projection = (k, d) @ (d, n) @ (n, d) @ (d, k)
        kernel, bias = fit_gram(XTX, XTY, normalize=normalize, projection=projection, alpha=alpha)

        loc = XTX.mean if normalize else None
        scale = XTX.std if normalize else None

        model_def = PCR.partial(
            history_len=history_len,
            projection=projection,
            output_dim=output_dim,
            loc=loc,
            scale=scale,
            history=history,
            name=name,
        )

        if key is None:
            key = random.generate_key()

        with flax.nn.stateful() as state:
            _, params = model_def.init_by_shape(key, [(1, input_dim)])

        model = flax.nn.Model(model_def, params)
        model.params["Linear"]["kernel"] = kernel
        model.params["Linear"]["bias"] = bias

        return model, state
