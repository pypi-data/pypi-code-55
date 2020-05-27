"""usual preprocessing on data"""

from typing import Pattern
import re
import pandas as pd

import logging


def explode_ts(df, col: str, pattern: re) -> pd.DataFrame:
    """split ts like '2020-03-25 13:56:40,848' in components

    add time components as int and remove initial col
    """
    if 'year' in df:
        logging.warning(
            'there is already dt related cols(year). Already applied?')
        return df
    ts = df[col]
    return pd.concat([df.drop(columns=col), ts.str.extract(pattern)], axis=1)
