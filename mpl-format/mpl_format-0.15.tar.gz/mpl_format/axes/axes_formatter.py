from pathlib import Path

from matplotlib.axes import Axes
from typing import Optional, Union, Dict, Callable

from mpl_format.axes.axis_formatter import AxisFormatter
from mpl_format.axes.axis_utils import new_axes
from mpl_format.io_utils import save_plot
from mpl_format.text.text_formatter import TextFormatter
from mpl_format.text.text_utils import wrap_text


class AxesFormatter(object):

    def __init__(self, axes: Optional[Axes] = None,
                 width: Optional[int] = None, height: Optional[int] = None):
        """
        Create a new AxesFormatter

        :param axes: The matplotlib Axes instance to wrap.
        """
        if axes is None:
            self._axes: Axes = new_axes(width=width, height=height)
        else:
            self._axes: Axes = axes

    @property
    def axes(self) -> Axes:
        """
        Return the wrapped Axes instance.
        """
        return self._axes

    @property
    def x_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the x-axis of the wrapped Axes.
        """
        return AxisFormatter(self._axes.xaxis)

    @property
    def y_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the y-axis of the wrapped Axes.
        """
        return AxisFormatter(self._axes.yaxis)

    @property
    def title(self) -> TextFormatter:
        return TextFormatter(self._axes.title)

    def set_title_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text of the Axes title.
        """
        self._axes.set_title(label=text)
        return self

    def set_title_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the title of the wrapped Axes.
        """
        self._axes.set_title(self._axes.get_title(), fontsize=font_size)
        return self

    def set_x_label_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.
        """
        self.x_axis.set_label_size(font_size)
        return self

    def set_x_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the x-axis label.
        """
        self.x_axis.set_label_text(text)
        return self

    def set_y_label_size(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.
        """
        self.y_axis.set_label_size(font_size)
        return self

    def set_y_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the y-axis label.
        """
        self.y_axis.set_label_text(text)
        return self

    def set_tick_label_sizes(self, font_size: int) -> 'AxesFormatter':
        """
        Set the font size for the tick labels of the wrapped Axes.
        """
        self.x_axis.set_label_size(font_size)
        self.y_axis.set_label_size(font_size)
        return self

    def set_font_sizes(
            self,
            title: Optional[int] = None,
            axis_labels: Optional[int] = None,
            x_axis_label: Optional[int] = None, y_axis_label: Optional[int] = None,
            tick_labels: Optional[int] = None,
            x_tick_labels: Optional[int] = None, y_tick_labels: Optional[int] = None,
            legend: Optional[int] = None,
            figure_title: Optional[int] = None
    ) -> 'AxesFormatter':

        ax = self._axes
        if title is not None:
            self.set_title_size(title)
        if axis_labels is not None:
            self.x_axis.set_label_size(axis_labels)
            self.y_axis.set_label_size(axis_labels)
        if x_axis_label is not None:
            self.x_axis.set_label_size(x_axis_label)
        if y_axis_label is not None:
            self.y_axis.set_label_size(y_axis_label)
        if tick_labels is not None:
            self.set_tick_label_sizes(tick_labels)
        if x_tick_labels is not None:
            self.x_axis.set_tick_label_size(x_tick_labels)
        if y_tick_labels is not None:
            self.y_axis.set_tick_label_size(y_tick_labels)
            ax.tick_params(axis='y', labelsize=y_tick_labels)
        if legend is not None:
            ax.legend(fontsize=legend)
        if figure_title is not None:
            ax.set_title(ax.get_title(), fontsize=title)

        return self

    def set_text(self, title: Optional[str] = None,
                 x_label: Optional[str] = None,
                 y_label: Optional[str] = None) -> 'AxesFormatter':
        """
        Set text properties for elements of the Axes.

        :param title: Text for the title.
        :param x_label: Text for the x-axis label.
        :param y_label: Text for the y-axis label.
        """
        if title is not None:
            self.set_title_text(title)
        if x_label is not None:
            self.x_axis.set_label_text(x_label)
        if y_label is not None:
            self.y_axis.set_label_text(y_label)
        return self

    def remove_legend(self) -> 'AxesFormatter':
        """
        Remove the legend from the Axes.
        """
        self._axes.get_legend().remove()
        return self

    def map_tick_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'AxesFormatter':
        """
        Map the tick label text using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_tick_labels(mapping)
        self.y_axis.map_tick_labels(mapping)
        return self

    def map_x_tick_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'AxesFormatter':
        """
        Map the tick label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_tick_labels(mapping)
        return self

    def map_y_tick_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'AxesFormatter':
        """
        Map the tick label text for the y-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.y_axis.map_tick_labels(mapping)
        return self

    def set_x_lim(self, left: Optional[float] = None, right: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the x-axis.

        :param left: Lower limit.
        :param right: Upper limit.
        """
        self._axes.set_xlim(left=left, right=right)
        return self

    def set_y_lim(self, bottom: Optional[float] = None, top: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the x-axis.

        :param bottom: Lower limit.
        :param top: Upper limit.
        """
        self._axes.set_ylim(bottom=bottom, top=top)
        return self

    def grid(self, value: bool, which: str = 'major', axis: str = 'both') -> 'AxesFormatter':
        """
        Turn the grid on or off.

        :param value: True or False
        :param which: 'major', 'minor' or 'both'
        :param axis: 'x', 'y' or 'both
        """
        self._axes.grid(b=value, which=which, axis=axis)
        return self

    def set_axis_below(self, value: bool) -> 'AxesFormatter':
        """
        Set whether axis ticks and gridlines are above or below most artists.
        """
        self._axes.set_axisbelow(b=value)
        return self

    def save(self, file_path: Union[str, Path], file_type: str = 'png') -> 'AxesFormatter':
        """
        Save the plot to disk.

        :param file_path: The file path to save the plot object to.
        :param file_type: The type of file to save.
        """
        save_plot(plot_object=self._axes, file_path=file_path, file_type=file_type)

    def tight_layout(self) -> 'AxesFormatter':
        """
        Call the tight_layout method on the Axes' figure.
        """
        self._axes.figure.tight_layout()
        return self

    def rotate_x_tick_labels(self, rotation: int, how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.x_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    def rotate_y_tick_labels(self, rotation: int, how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the y-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.y_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    def remove_x_ticks(self) -> 'AxesFormatter':
        """
        Remove x-ticks from the Axes.
        """
        self._axes.set_xticks([])
        return self

    def remove_y_ticks(self) -> 'AxesFormatter':
        """
        Remove y-ticks from the Axes.
        """
        self._axes.set_yticks([])
        return self

    def invert_x_axis(self) -> 'AxesFormatter':
        """
        Invert the x-axis.
        """
        self.x_axis.invert()
        return self

    def invert_y_axis(self) -> 'AxesFormatter':
        """
        Invert the y-axis.
        """
        self.y_axis.invert()
        return self

    def wrap_x_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the x-axis with new lines if it exceeds
        a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_y_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the y-axes with new lines if it exceeds
        a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.y_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on each axis with new lines if it exceeds
        a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_tick_labels(max_width=max_width)
        self.y_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_title(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the title if it exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.set_title_text(wrap_text(self.title.text, max_width=max_width))
        return self
