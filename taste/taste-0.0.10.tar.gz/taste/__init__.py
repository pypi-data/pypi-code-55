from operator import itemgetter
from typing import Iterable, Optional
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

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
            grid: bool = False,
            grid_options: dict = None,
            origin_lines: bool = False,
            origin_lines_options: dict = None,
            bar_label: str = None, value_label: str = None,
            bar_axis_labels: Iterable = None,
            bar_axis_rotation: float = 0,
            value_axis_labels: Iterable = None,
            value_axis_rotation: float = 0,
            value_top_labels: Iterable = None,
            value_top_rotation: float = 0,
            value_top_offset: float = 0.2,
            title: str = None, title_options: dict = None,
            caption: str = None, caption_options: dict = None,
            legend: bool = False, legend_options: dict = None,
            legend_detect: str = "auto", plot_options: dict = None,
            orientation: str = VT
    ):
        # matplotlib.org/api/_as_gen/matplotlib.pyplot.bar.html
        # matplotlib.org/api/_as_gen/matplotlib.pyplot.barh.html
        plot_options = plot_options or {"label": "BarPlot"}

        # matplotlib.org/api/_as_gen/matplotlib.axes.Axes.grid.html
        grid_options = grid_options or {}

        # matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html
        # but is kind of useless *before* the references are created in its
        # original shape, therefore legend_detect manipulates legend() calls:
        #
        # auto        -> 1st option, fetch label from plot instance
        # all_bars    -> 2nd option, fetch all bar refs in order, map labels
        #                -> "labels" key in legend_options is required now
        #                   but defaults to bar labels on axis
        # select_bars -> 2nd option, but allows selecting bars with index
        #                -> {"handles": [0, 2, 4], "labels": ["a", "b", "c"]}
        # manual -> 3rd option, handles (refs) + labels passed directly
        legend_options = legend_options or {"labels": bar_axis_labels}

        # matplotlib.org/api/_as_gen/matplotlib.axes.Axes.axvline.html
        # matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html
        origin_lines_options = origin_lines_options or {"x": {}, "y": {}}

        # matplotlib.org/api/_as_gen/matplotlib.pyplot.suptitle.html
        caption_options = caption_options or {
            "fontsize": 14, "fontweight": "bold"
        }

        # matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html
        title_options = title_options or {}

        with AggBackend(), FigureContext() as fig:
            self.figure = fig

            if orientation == VT:
                plt.bar(x=bars, height=values, **plot_options)
            elif orientation == HT:
                plt.barh(y=bars, width=values, **plot_options)
            else:
                raise Exception(f"Invalid orientation {orientation}")

            ax = self.figure.axes[0]

            # grid lines
            ax.grid(grid, **grid_options)

            # all labels
            self.draw_labels(
                ax=ax, bar=bar_label, value=value_label,
                bar_axis=bar_axis_labels, value_axis=value_axis_labels,
                bar_axis_rotation=bar_axis_rotation,
                value_axis_rotation=value_axis_rotation,
                value_top=value_top_labels, value_top_offset=value_top_offset,
                value_top_rotation=value_top_rotation, orientation=orientation
            )

            # major figure/plot title
            if caption:
                self.figure.suptitle(caption, **caption_options)

            # minor title for a single plot via Axes object
            if title:
                ax.set_title(title, **title_options)

            # lines crossed on [0, 0]
            if origin_lines:
                ax.axvline(x=0, **origin_lines_options["x"])
                ax.axhline(y=0, **origin_lines_options["y"])

            lopts = legend_options
            if legend and legend_detect == "auto":
                ax.legend()
            elif legend and legend_detect == "all_bars":
                ax.legend(handles=ax.patches, **lopts)
            elif legend and legend_detect == "select_bars":
                ax.legend(
                    handles=itemgetter(*lopts["handles"])(ax.patches),
                    labels=lopts["labels"]
                )
            elif legend and legend_detect == "manual":
                ax.legend(**lopts)

    def draw_labels(
            self, ax: Axes, bar: Optional[str], value: Optional[str],
            bar_axis: Optional[Iterable], value_axis: Optional[Iterable],
            bar_axis_rotation: float, value_axis_rotation: float,
            value_top: Optional[Iterable], value_top_offset: float,
            value_top_rotation: float, orientation: str = VT
    ):
        # horizontal label
        if orientation == HT:
            if bar:
                ax.set_ylabel(bar)
            if value:
                ax.set_xlabel(value)
            if bar_axis:
                ax.set_yticks(range(len(bar_axis)))
                ax.set_yticklabels(bar_axis, rotation=bar_axis_rotation)
            if value_axis:
                ax.set_xticklabels(value_axis, rotation=value_axis_rotation)

        # vertical label
        elif orientation == VT:
            if bar:
                ax.set_xlabel(bar)
            if value:
                ax.set_ylabel(value)
            if bar_axis:
                ax.set_xticks(range(len(bar_axis)))
                ax.set_xticklabels(bar_axis, rotation=bar_axis_rotation)
            if value_axis:
                ax.set_yticklabels(value_axis, rotation=value_axis_rotation)

        if value_top:
            self.draw_bar_top(
                ax=ax, values=value_top, offset=value_top_offset,
                orientation=orientation, rotation=value_top_rotation
            )

    def draw_bar_top(
            self, ax: Axes, values: Iterable, offset: float,
            rotation: float, orientation: str = VT
    ):
        attr_x = attr_x_start = attr_y = attr_y_start = None

        if orientation == VT:
            attr_y = "get_height"
            attr_y_start = "get_y"
            attr_x = "get_width"
            attr_x_start = "get_x"
        elif orientation == HT:
            attr_x = "get_height"
            attr_x_start = "get_y"
            attr_y = "get_width"
            attr_y_start = "get_x"

        for bar, val in zip(ax.patches, values):
            height = getattr(bar, attr_y)()
            pos = [
                getattr(bar, attr_x_start)() + getattr(bar, attr_x)() / 2.0,
                height + offset * height / abs(height)  # mirror on origin
            ]

            if orientation == HT:
                pos = pos[-1::-1]  # swap values

            ax.text(
                x=pos[0], y=pos[1], s=val, ha="center",
                va="center", rotation=rotation
            )
