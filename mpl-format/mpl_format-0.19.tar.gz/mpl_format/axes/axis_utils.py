import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def new_axes(width: int = None, height: int = None) -> Axes:
    """
    Return new matplotlib axes.
    """
    width = width or 16
    height = height or 9
    _, ax = plt.subplots(figsize=(width, height))
    return ax
