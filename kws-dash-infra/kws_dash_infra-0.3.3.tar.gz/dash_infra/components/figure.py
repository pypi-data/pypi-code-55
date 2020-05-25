from dash_core_components import Graph
from dash_infra.core import as_callback, as_component

from .store_user import StoreUser


class Figure(StoreUser):
    """
    A Figure component uses a Storage Component as a temporary
    output for all registered callback inputs.
    Each output is stored as a key in the state of the output
    and can be accessed as a dataset.
    """

    def __init__(self, id, store=None, layout=None, **kwargs):
        super().__init__(
            id,
            display_component=Graph,
            display_properties="figure",
            store=store,
            **kwargs,
        )
        self.graph_layout = layout

    def display(self, data):
        graph = {
            "data": data,
            "layout": self.graph_layout,
        }
        return graph


class PandasFigure(Figure):
    def __init__(self, id, dataset_config, types=None, names=None, **kwargs):
        super().__init__(id, **kwargs)
        self.dataset_config = dataset_config

    def _get_col(self, df, label):
        if isinstance(label, int):
            return df.columns[label]
        return label

    def _process_data(self, data):
        datasets = []
        for dataset_name, config in self.dataset_config.items():
            dataset = data[dataset_name]
            x_cols = config.get("x_cols", [])
            y_cols = config.get("y_cols", [])
            types = config.get("types", ["markers"] * len(x_cols))
            names = config.get(
                "names",
                [
                    f"{self._get_col(dataset, x)} vs {self._get_col(dataset, y)}"
                    for (x, y) in zip(x_cols, y_cols)
                ],
            )

            datasets += [
                {
                    "x": list(dataset[self._get_col(dataset, x)]),
                    "y": list(dataset[self._get_col(dataset, y)]),
                    "mode": t,
                    "name": name,
                }
                for x, y, t, name in zip(x_cols, y_cols, types, names)
            ]

        return datasets
