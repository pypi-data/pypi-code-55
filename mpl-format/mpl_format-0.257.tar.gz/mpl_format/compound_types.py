from matplotlib.axes import Axes
from matplotlib.figure import Figure
from seaborn import JointGrid, PairGrid
from typing import TypeVar, Tuple

PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)
Color = TypeVar('Color', str, Tuple[float, float, float, float])
FontSize = TypeVar('FontSize', str, float, int)
LegendLocation = TypeVar('LegendLocation', str, Tuple[float, float])
