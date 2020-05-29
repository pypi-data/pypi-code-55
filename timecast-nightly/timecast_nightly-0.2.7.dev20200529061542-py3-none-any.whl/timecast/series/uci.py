"""timecast.series.uci"""
import os
from typing import Tuple

import numpy as np

from timecast.series._core import generate_timeline


def generate(path=None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Description: Outputs various weather metrics from a UCI dataset from 13/3/2012 to 11/4/2012

    References:
        * https://archive.ics.uci.edu/ml/machine-learning-databases/00274/NEW-DATA.zip
    """

    return generate_timeline(
        path=path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/uci.txt"),
        name="7:CO2_Habitacion_Sensor",
        delimiter=" ",
    )
