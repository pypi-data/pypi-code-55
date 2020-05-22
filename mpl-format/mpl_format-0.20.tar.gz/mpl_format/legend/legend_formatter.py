from matplotlib.legend import Legend
from typing import Union

from mpl_format.text.text_formatter import TextFormatter


class LegendFormatter(object):

    def __init__(self, legend: Legend):
        """
        Create a new legend formatter.
        """
        self._legend: Legend = legend

    @property
    def legend(self) -> Legend:
        return self._legend

    @property
    def title(self) -> TextFormatter:
        """
        Return a TextFormatter around the legend's title.
        """
        return TextFormatter(self._legend.get_title())

    # region set location

    def set_location(self, location: Union[int, str]) -> 'LegendFormatter':
        """
        Set the legend location.
        """
        self._legend._set_loc(location)
        return self

    def set_location_best(self) -> 'LegendFormatter':
        """
        Set the legend location to 'best'.
        """
        self.set_location('best')
        return self

    def set_location_upper_left(self) -> 'LegendFormatter':
        """
        Set the legend location to 'upper left'.
        """
        self.set_location('upper left')
        return self

    def set_location_upper_center(self) -> 'LegendFormatter':
        """
        Set the legend location to 'upper center'.
        """
        self.set_location('upper center')
        return self

    def set_location_upper_right(self) -> 'LegendFormatter':
        """
        Set the legend location to 'upper right'.
        """
        self.set_location('upper right')
        return self

    def set_location_center_left(self) -> 'LegendFormatter':
        """
        Set the legend location to 'center left'.
        """
        self.set_location('center left')
        return self

    def set_location_center(self) -> 'LegendFormatter':
        """
        Set the legend location to 'center'.
        """
        self.set_location('center')
        return self

    def set_location_center_right(self) -> 'LegendFormatter':
        """
        Set the legend location to 'center right'.
        """
        self.set_location('center right')
        return self

    def set_location_lower_left(self) -> 'LegendFormatter':
        """
        Set the legend location to 'lower left'.
        """
        self.set_location('lower left')
        return self

    def set_location_lower_center(self) -> 'LegendFormatter':
        """
        Set the legend location to 'lower center'.
        """
        self.set_location('lower center')
        return self

    def set_location_lower_right(self) -> 'LegendFormatter':
        """
        Set the legend location to 'lower right'.
        """
        self.set_location('lower right')
        return self

    def set_location_left(self) -> 'LegendFormatter':
        """
        Set the legend location to 'center left'.
        """
        self.set_location('center left')
        return self

    def set_location_right(self) -> 'LegendFormatter':
        """
        Set the legend location to 'center right'.
        """
        self.set_location('center right')
        return self

    # endregion
