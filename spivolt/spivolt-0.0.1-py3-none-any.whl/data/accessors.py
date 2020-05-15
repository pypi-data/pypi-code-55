import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Optional


@pd.api.extensions.register_dataframe_accessor("sp")
class SpAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj.sort_values(["time", "pot_number"])

    @staticmethod
    def _validate(obj):
        if "potential" not in obj.columns:
            raise AttributeError("Must have 'potential' field.")
        elif "pot_number" not in obj.columns:
            raise AttributeError("Must have 'pot_number' field.")

    def between(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> pd.DataFrame:
        data = self._obj.copy()
        if start:
            data = data[data["time"] >= start]
        if end:
            data = data[data["time"] <= end]
        return data

    def potwise(self) -> pd.DataFrame:
        return self._obj.pivot(index="time", columns="pot_number", values="potential")

    def plot(self, figsize=(13, 50)):
        sensor_list = self._obj.pot_number.unique()
        fig, ax = plt.subplots(nrows=len(sensor_list), ncols=1, figsize=figsize)
        for current_pot in sensor_list:
            data = self._obj[self._obj.pot_number == current_pot]
            idx = np.where(sensor_list == current_pot)[0][0]
            ax[idx].plot(data.time, data.potential)
            ax[idx].set_title(f"SP: Pot {current_pot}")
            ax[idx].set_ylabel("Potential (mV)")
        fig.tight_layout()
