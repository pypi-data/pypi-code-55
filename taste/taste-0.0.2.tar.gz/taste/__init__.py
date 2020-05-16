from typing import Iterable
import matplotlib.pyplot as plt

VT = "vertical"
HT = "horizontal"

class AggBackend:
    def __enter__(self):
        self.old_backend = plt.get_backend()
        plt.switch_backend("Agg")

    def __exit__(self, *_, **__):
        plt.switch_backend(self.old_backend)


class FigureCleanMixin:
    def __del__(self):
        if not hasattr(self, "figure"):
            return
        plt.close(self.figure)


class BarPlot(FigureCleanMixin):
    def __init__(
            self, bars, values,
            bar_label: str = None, value_label: str = None,
            orientation: str = VT
    ):
        with AggBackend():
            self.figure = plt.figure()

            if orientation == VT:
                plt.bar(x=bars, height=values)
            elif orientation == HT:
                plt.barh(y=bars, width=values)
            else:
                raise Exception(f"Invalid orientation {orientation}")

            # horizontal label
            if orientation == HT:
                if bar_label:
                    self.figure.axes[0].set_ylabel(bar_label)
                if value_label:
                    self.figure.axes[0].set_xlabel(value_label)

            # vertical label
            elif orientation == VT:
                if bar_label:
                    self.figure.axes[0].set_xlabel(bar_label)
                if value_label:
                    self.figure.axes[0].set_ylabel(value_label)
