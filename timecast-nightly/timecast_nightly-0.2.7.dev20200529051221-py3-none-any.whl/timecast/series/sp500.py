"""timecast.series.sp500"""
import os
from typing import Tuple

import numpy as np

from timecast.series._core import generate_timeline


def generate(path=None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Description: Outputs the log-normalized daily opening price of the S&P 500
    stock market index from January 3, 1986 to June 29, 2018.
    """

    return generate_timeline(
        path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/sp500.csv")
    )
