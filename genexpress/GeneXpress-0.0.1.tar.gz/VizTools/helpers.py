import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.lines import Line2D
import seaborn as sns
import chart_studio.tools
import plotly.graph_objs as go
import numpy as np
import pandas as pd



def add_tick_labels(ax, labels, x_ticks=True, rotation=45):
    if x_ticks:
        ax.set_xticklabels(labels=labels, rotation=rotation)
        # ax.xaxis.set_ticklabels()
    else:
        ax.set_yticklabels(labels=labels, rotation=rotation)


def add_extended_ticks(ax, tick_len=6, x_ticks=True, rotation=45):
    if x_ticks:
        # may have to change this to get_majorticklabels??
        tick_labels = ax.get_xticklabels()
    else:
        tick_labels = ax.get_yticklabels()
    newticklabels = [l if not i % 2 else ('_'*tick_len+" " + l)
                      for i, l in enumerate([label.get_text()
                      for label in tick_labels])]
    add_tick_labels(ax, newticklabels, x_ticks=x_ticks, rotation=45)


def set_text_size(text, size):
    for item in text:
        item.set_fontsize(size)

def make_markers(size):
    mpl_markers = []
    for k,v in Line2D.markers.items():
        if v != 'nothing':
            mpl_markers.append(k)
    markers = mpl_markers + ["$:)$", "$:($", "$=$", "$?$", "$!$"]

    if size > len(markers):
        mult = size/len(markers)
        mod = size%len(markers)
        if mod == 0:
            markers = markers*int(mult)
        else:
            markers = markers*int((mult+1))
    else:
        markers = markers[:size]



def make_colors(size, colormap='plasma'):
    cm = plt.get_cmap(colormap)
    colors = [cm(1. * i / size) for i in range(size)]
    return colors


def construct_point(size):
    """
    Assign symbol and color for each point for a matplotlib scatter plot (2D or 3D)
    Args:
        size: number of samples in the data

    Returns:

    """
    markers = ['o', 'v', 's', 'd', 'P', '+', '8', '*', "X", 'x', "D", 'd', 7, 6,
               "$:)$", "$:($", "$=$", "$?$",
               "$!$"]
    if size > len(markers):
        mult = size/len(markers)
        mod = size%len(markers)
        if mod == 0:
            markers = markers*int(mult)
        else:
            markers = markers*int((mult+1))
    cm = plt.get_cmap('plasma')
    colors = [cm(1. * i / size) for i in range(size)]
    return markers, colors


def save_online_interactive(fig: go.Figure, name):
    """
    Save an interactive plotly plot on my account
    Args:
        fig: a go.Figure object to save online
        name: a name for the plot

    """
    from chart_studio.plotly import plot
    if chart_studio.tools.get_credentials_file().get('username') != 'coltongarelli':
        chart_studio.tools.set_credentials_file(username='coltongarelli', api_key='JEoo9aVmctpeUlByHPU3')
    plot(fig, filename=name, auto_open=True)


def save_local_interactive(fig: go.Figure, name):
    """
    Save an interactive plotly plot locally
    Args:
        fig: a go.Figure object to save online
        name: a name for the plot

    """
    from plotly.offline import plot
    plot(fig, filename=name)


def add_plot(df, ax, rows):
    markers, colors = construct_point(df.shape[0])
    cdict = dict(zip(rows.keys(), colors))
    marker = dict(zip(rows.keys(), markers))
    labels = df.index.to_list()
    for k, v in rows.items():
        ax.scatter(xs=df.loc[v]['Principal Component 1'], ys=df.loc[v]['Principal Component 2'], zs=df.loc[v]['Principal Component 3'],
                   c=[cdict.get(k)],
                   marker=marker.get(k), label=labels[k],
                   s=55)


class MidpointNormalize(colors.Normalize):
    """
    Copied from: http://chris35wills.github.io/matplotlib_diverging_colorbar/
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)

    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))


def create_diagonal_trues(df):
    filler = np.zeros(df.shape, dtype=bool)
    np.fill_diagonal(filler, 1)
    filters = pd.DataFrame(index=df.index, columns=df.index, data=filler)
    return filters


def make_midpoint_mappable(max, min, cmap='inferno'):
    if cmap is None:
        cmap = sns.diverging_palette(h_neg=250, h_pos=10, as_cmap=True)
    if max > 6:
        max = 6
    if min < -6:
        min = -6
    midnorm = MidpointNormalize(midpoint=0, vmin=min, vmax=max)
    return plt.cm.ScalarMappable(cmap=cmap, norm=midnorm)


class MidpointNormalize(colors.Normalize):
    """Taken from https://matplotlib.org/3.1.0/gallery/userdemo/colormap_normalizations_custom.html

    Normalize colorscale to midpoint (such as 0) rather than the center of the data
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


