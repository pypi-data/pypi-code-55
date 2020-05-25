import os

import pandas as pd
import plotly.express as px

from .figure import Figure


class PandasScatterMap(Figure):
    """
    A special figure used to display a scatter map.
    """

    def __init__(
        self,
        id: str,
        key: str,
        mapbox_token: str,
        dataset_config: dict = None,
        **kwargs
    ):
        dataset_config = dataset_config or None
        super().__init__(id, keys=[key], **kwargs)
        self.dataset_config = dataset_config
        self.mapbox_token = mapbox_token

    def _process_data(self, data):
        return data[self.keys[0]]

    def display(self, df):
        px.set_mapbox_access_token(self.mapbox_token)
        if df.empty:
            dummy = pd.DataFrame(dict(lat=[0], lon=[0]))
            return px.scatter_mapbox(
                dummy, "lat", "lon", mapbox_style="white-bg"
            ).to_dict()
        fig = px.scatter_mapbox(df, **self.dataset_config)
        fig_dict = fig.to_dict()
        return fig_dict
