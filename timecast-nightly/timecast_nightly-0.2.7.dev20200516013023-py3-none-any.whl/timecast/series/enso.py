"""timecast.series.enso"""
import os
from typing import Tuple

import jax.numpy as jnp
import numpy as np
import pandas as pd


def generate(input_signals=None, output_signals=None, path=None) -> Tuple[np.ndarray, np.ndarray]:
    """Generate ENSO

    Description: Collection of monthly values of control indices useful for predicting
    La Nina/El Nino. More specifically, the user can choose any of pna, ea,
    wa, wp, eu, soi, esoi, nino12, nino34, nino4, oni of nino34 (useful for
    La Nino/El Nino identification) to be used as input and/or output in
    the problem instance.
    """

    input_signals = input_signals or [
        "pna",
        "ea",
        "wa",
        "wp",
        "eu",
        "soi",
        "esoi",
        "nino12",
        "nino34",
        "nino4",
    ]
    output_signals = output_signals or ["oni"]
    data = pd.read_csv(
        path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/enso.csv")
    )
    signal_length = data.shape[0]

    # Get climatology
    clm = jnp.asarray(data.nino34).reshape(-1, 12).mean(axis=0)

    # Compute anomaly
    data["anm"] = (jnp.asarray(data.nino34).reshape(-1, 12) - clm).reshape(signal_length)

    # Get ONI
    data["oni"] = jnp.asarray(data.anm.rolling(3, min_periods=1).mean())
    data["month"] = jnp.arange(signal_length) % 12

    return (
        jnp.asarray(data[input_signals]),
        jnp.asarray(data[output_signals]).reshape(-1, 1),
    )
