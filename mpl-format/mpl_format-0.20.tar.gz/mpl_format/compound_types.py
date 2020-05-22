from matplotlib.axes import Axes
from matplotlib.figure import Figure
from seaborn import JointGrid, PairGrid
from typing import TypeVar

PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)
