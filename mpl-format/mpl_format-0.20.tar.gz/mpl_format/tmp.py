import matplotlib.pyplot as plt
from numpy.ma import arange

from mpl_format.axes.axes_formatter import AxesFormatter
from mpl_format.axes.axis_utils import new_axes

x = arange(0, 1.01, 0.05)
y = x ** 2


ax = new_axes()
ax.plot(x, y)
AxesFormatter(ax).x_axis.set_format_percent(1)
plt.show()
