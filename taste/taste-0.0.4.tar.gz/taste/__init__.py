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


class FigureContext:
    def __init__(self, figure=None, old_on_enter=False):
        self.old_on_enter = old_on_enter
        self.old_figure = None

        if not self.old_on_enter:
            self.old_figure = plt.gcf()

        self.figure = figure or plt.figure()

    def __enter__(self):
        if self.old_on_enter:
            self.old_figure = plt.gcf()
        plt.figure(self.figure.number)
        return self.figure

    def __exit__(self, *_, **__):
        plt.figure(self.old_figure.number)
        if self.old_on_enter:
            self.old_figure = None


class FigureCleanMixin:
    def __del__(self):
        if not hasattr(self, "figure"):
            return
        plt.close(self.figure)


class BarPlot(FigureCleanMixin):
    def __init__(
            self, bars, values,
            bar_label: str = None, value_label: str = None,
            bar_axis_labels: Iterable = None,
            value_axis_labels: Iterable = None,
            title: str = None, orientation: str = VT
    ):
        with AggBackend(), FigureContext() as fig:
            self.figure = fig

            if orientation == VT:
                plt.bar(x=bars, height=values)
            elif orientation == HT:
                plt.barh(y=bars, width=values)
            else:
                raise Exception(f"Invalid orientation {orientation}")

            ax = self.figure.axes[0]
            # horizontal label
            if orientation == HT:
                if bar_label:
                    ax.set_ylabel(bar_label)
                if value_label:
                    ax.set_xlabel(value_label)
                if bar_axis_labels:
                    ax.set_yticks(range(len(bar_axis_labels)))
                    ax.set_yticklabels(bar_axis_labels)
                if value_axis_labels:
                    ax.set_xticklabels(value_axis_labels)

            # vertical label
            elif orientation == VT:
                if bar_label:
                    ax.set_xlabel(bar_label)
                if value_label:
                    ax.set_ylabel(value_label)
                if bar_axis_labels:
                    ax.set_xticks(range(len(bar_axis_labels)))
                    ax.set_xticklabels(bar_axis_labels)
                if value_axis_labels:
                    ax.set_yticklabels(value_axis_labels)

            if title:
                ax.set_title(title)
