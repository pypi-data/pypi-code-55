from pathlib import Path

from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import ndarray
from typing import Tuple, Union, Dict, Callable, List

from mpl_format.axes.axes_formatter import AxesFormatter
from mpl_format.axes.axes_formatter_array import AxesFormatterArray
from mpl_format.io_utils import save_plot


class FigureFormatter(object):

    share_values = ('all', 'row', 'col', 'none')

    def __init__(self, axes: Axes = None,
                 n_rows: int = 1, n_cols: int = 1,
                 fig_size: Tuple[int, int] = (16, 9),
                 share_x: str = 'none',
                 share_y: str = 'none'):

        if axes is not None:
            self._figure: Figure = axes.figure
            self._axes = axes
        else:
            assert share_x in self.share_values
            assert share_y in self.share_values
            self._fig_size: Tuple[int, int] = fig_size
            figure, axes = plt.subplots(nrows=n_rows, ncols=n_cols,
                                        sharex=share_x, sharey=share_y,
                                        figsize=fig_size)
            self._axes: Union[Axes, ndarray] = axes
        self._has_array = isinstance(self._axes, ndarray)

    @property
    def axes(self) -> Union[AxesFormatter, AxesFormatterArray]:
        """
        Return an AxesFormatter or AxesFormatterArray for the wrapped Axes or array of Axes.
        """
        if not self._has_array:
            return AxesFormatter(self._axes)
        else:
            return AxesFormatterArray(self._axes)

    @property
    def single(self) -> AxesFormatter:
        """
        Return an AxesFormatter for the wrapped Axes.
        """
        if not self._has_array:
            return AxesFormatter(self._axes)
        else:
            raise TypeError('FigureFormatter holds an array of Axes.')

    @property
    def multi(self) -> AxesFormatterArray:
        """
        Return an AxesFormatterArray for the wrapped Axes.
        """
        if self._has_array:
            return AxesFormatterArray(self._axes)
        else:
            raise TypeError('FigureFormatter holds a single Axes.')

    def set_axes_title_text(
            self,
            text: Union[str, List[str], Callable[[int, int], str], Callable[[int], str]]
    ) -> 'FigureFormatter':
        """
        Set the title of each Axes using a string, list of strings or function that returns a string based on the
        row and column or the flat index of the Axes.

        :param text: Title or titles to set
        """
        if not self._has_array:
            if not isinstance(text, str):
                raise TypeError('text must be a str for a single Axes.')
            else:
                self.single.set_title_text(text)
        else:
            if isinstance(text, str):
                for axf in self.multi.flat:
                    axf.set_title_text(text)
            elif isinstance(text, list):
                if len(text) != self.multi.size:
                    raise ValueError(f'There are {self.multi.size} Axes and {len(text)} labels.')
                else:
                    for axf, t in zip(self.multi.flat, text):
                        axf.set_title_text(t)
            elif callable(text):
                try:
                    for row in range(self.multi.shape[0]):
                        for col in range(self.multi.shape[1]):
                            self.multi[row, col].set_title_text(text(row, col))
                except TypeError:
                    for a, axf in enumerate(self.multi.flat):
                        axf.set_title_text(text(a))
            else:
                raise TypeError(f'Wrong type passed to set_axes_title_text: {type(text)}')
        return self

    def map_axes_title_text(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'FigureFormatter':
        """
        Map the label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if not self._has_array:
            self.single.map_title_text(mapping=mapping)
        else:
            for axf in self.multi.flat:
                axf.map_title_text(mapping=mapping)
        return self

    def remove_x_axis_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.remove_x_label()
        else:
            self.single.remove_x_label()
        return self

    def remove_y_axis_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.remove_y_label()
        else:
            self.single.remove_y_label()
        return self

    def remove_axes_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        self.remove_x_axis_labels()
        self.remove_y_axis_labels()
        return self

    def map_x_axis_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'FigureFormatter':
        """
        Map the label text for each x-axis in the Figure using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.map_x_axis_label(mapping=mapping)
        else:
            self.single.map_x_axis_label(mapping=mapping)
        return self

    def map_y_axis_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'FigureFormatter':
        """
        Map the label text for each y-axis in the Figure using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.map_y_axis_label(mapping=mapping)
        else:
            self.single.map_y_axis_label(mapping=mapping)
        return self

    def map_axes_labels(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'FigureFormatter':
        """
        Map the label text for each axis in the Figure using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_axis_labels(mapping=mapping)
        self.map_y_axis_labels(mapping=mapping)
        return self

    def save(self, file_path: Union[str, Path], file_type: str = 'png') -> 'FigureFormatter':
        """
        Save the plot to disk.

        :param file_path: The file path to save the plot object to.
        :param file_type: The type of file to save.
        """
        save_plot(plot_object=self._figure, file_path=file_path, file_type=file_type)
        return self

    @staticmethod
    def show():
        """
        Show the figure.
        """
        plt.show()

    def __getitem__(self, *args, **kwargs) -> AxesFormatter:

        return self.multi.__getitem__(*args, **kwargs)
