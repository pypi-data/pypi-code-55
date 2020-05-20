"""
Plot functions enhancing Matplotlib
"""
from matplotlib import rcParams

rcParams["axes.axisbelow"] = False

# rcParams['font.family'] = 'sans-serif'
# rcParams['font.sans-serif'] = ['Arial'] # TODO
# rcParams['font.size'] = 14
# rcParams['text.usetex'] = True
# rcParams['text.latex.unicode'] = True

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib.transforms as trans
import matplotlib.colors as mcolors

from rwth_nb.plots import colors
import numpy as np


# Propagate rwth_colors to default matplotlib colors
mcolors.get_named_colors_mapping().update(colors.rwth_colors)

def axis(ax):
    """
    Decorate axes RWTH way.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes to be beautified


    See Also
    --------
    TODO
    
    Notes
    -----
    Nada.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import rwth_nb.plot.mpl_decorations as rwth_plt
    >>>
    >>> x = np.linspace(-5,5,100)
    >>> fig,ax = plt.subplots()
    >>> ax.plot(x, x**2)
    >>> ax.set_xlabel('x'); ax.set_ylabel('f(x)');
    >>> rwth_plt.axis(ax)
    """
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    def on_xlims_change(ax):
        # update x spine position to be always at zero, left or right according to set limits
        # update y-label x-position and horizontal alignment
        if (np.array(ax.get_xlim()) < 0).all():  # all limits negative
            left_spine_pos = ('axes', 1)
            ylabel_xpos = 1
            ylabel_halignment = 'right'
        elif (np.array(ax.get_xlim()) > 0).all():  # all limits positive
            left_spine_pos = ('axes', 0)  # spine at the left
            ylabel_xpos = 0
            ylabel_halignment = 'left'
        else:  # zero is in plot
            left_spine_pos = 'zero'  # spine at zero ([0, 0])
            xmin = ax.get_xlim()[0]
            xmax = ax.get_xlim()[1]
            ylabel_xpos = np.abs(xmin) / (np.abs(xmax) + np.abs(xmin))
            ylabel_halignment = 'left'

        ax.spines['left'].set_position(left_spine_pos)
        ax.yaxis.set_label_coords(ylabel_xpos, 1)
        ax.yaxis.label.set_horizontalalignment(ylabel_halignment)

    def on_ylims_change(ax):
        # update y spine position to be always at zero, top or bottom according to set limits
        # update x-label y-position
        if (np.array(ax.get_ylim()) < 0).all():  # all limits negative
            bottom_spine_pos = ('axes', 1)  # spine at the top
            xlabel_ypos = 1
        elif (np.array(ax.get_ylim()) > 0).all():  # all limits positive
            bottom_spine_pos = ('axes', 0)  # spine at the bottom
            xlabel_ypos = 0
        else:  # zero is in plot
            bottom_spine_pos = 'zero'  # spine at zero ([0, 0])
            ymin = ax.get_ylim()[0]
            ymax = ax.get_ylim()[1]
            xlabel_ypos = np.abs(ymin) / (np.abs(ymax) + np.abs(ymin))

        ax.spines['bottom'].set_position(bottom_spine_pos)
        ax.xaxis.set_label_coords(1, xlabel_ypos)

    ax.callbacks.connect('xlim_changed', on_xlims_change)
    ax.callbacks.connect('ylim_changed', on_ylims_change)

    on_xlims_change(ax)
    ax.xaxis.label.set_verticalalignment('bottom')
    ax.xaxis.label.set_horizontalalignment('right')

    ax.yaxis.label.set_rotation(0)
    on_ylims_change(ax)
    ax.yaxis.label.set_verticalalignment('top')
    ax.yaxis.label.set_horizontalalignment('left')

    ax.xaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontsize(12)


def twinx(ax, visible_spine='left'):
    """
    Create a twin Axes sharing the x-axis.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Existing Axes
    visible_spine: {'left', 'right'}, str, optional
        Position of the only visible axis spine

    Returns
    -------
    ax_twin: matplotlib.axes.Axes
        The newly created Axes instance

    See also
    --------
    matplotlib.axes.Axes.twinx
    twiny: Create a twin Axes sharing the y-axis.

    """
    if visible_spine in ['left', 'right']:
        # remove visible spine from hidden spine list
        hidden_spines = ['top', 'bottom', 'left', 'right']
        hidden_spines.remove(visible_spine)

        # create twiny and hide spines
        ax_twin = ax.twiny()
        for pos in hidden_spines:
            ax_twin.spines[pos].set_color('none')

        # set label position according to spine position (left/right, top)
        ax_twin.yaxis.set_label_coords(visible_spine == 'right', 1)

        return ax_twin
    else:
        # invalid keyword
        raise ValueError('Twin x-axis location must be either "left" or "right"')


def twiny(ax, visible_spine='top'):
    """
    Create a twin Axes sharing the y-axis.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Existing Axes
    visible_spine: {'top', 'bottom'}, str, optional
        Position of the only visible axis spine

    Returns
    -------
    ax_twin: matplotlib.axes.Axes
        The newly created Axes instance

    See also
    --------
    matplotlib.axes.Axes.twiny
    twinx: Create a twin Axes sharing the x-axis.
    """
    if visible_spine in ['top', 'bottom']:
        # remove visible spine from hidden spine list
        hidden_spines = ['top', 'bottom', 'left', 'right']
        hidden_spines.remove(visible_spine)

        # create twiny and hide spines
        ax_twin = ax.twiny()
        for pos in hidden_spines:
            ax_twin.spines[pos].set_color('none')

        # set label position according to spine position (right, bottom/top)
        ax_twin.xaxis.set_label_coords(1, visible_spine == 'top')

        return ax_twin
    else:
        # invalid keyword
        raise ValueError('Twin y-axis location must be either "top" or "bottom"')


def annotate_xtick(ax, txt, x, y=0, col='black', fs=12):
    """
    Annotate certain tick on the x-axis
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Current axes
    txt: string
        Annotated text
    x: float [scalar]
        x position of tick and txt
    y: float [scalar]
        y position of txt
        
    See Also
    --------
    annotate_ytick: Annotates a tick on the y-axis
    """
    txt_ret = ax.text(x, y, txt, color=col, fontsize=fs, verticalalignment='top', horizontalalignment='center',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.75))
    line_ret, = ax.plot([x, x], [0, y], '--', color=col, lw=0.5)
    return txt_ret, line_ret


def annotate_ytick(ax, txt, x, y, col='black', fs=12):
    """
    Annotate certain tick on the y-axis
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Current axes
    txt: string
        Annotated text
    x: float [scalar]
        x position of tick and txt
    y: float [scalar]
        y position of txt
        
    See Also
    --------
    annotate_yxtick: Annotates a tick on the x-axis
    """
    txt_ret = ax.text(x, y, txt, color=col, fontsize=fs, verticalalignment='top', horizontalalignment='center',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.75))
    line_ret, = ax.plot([0, x], [y, y], '--', color=col, lw=0.5)
    
    return txt_ret, line_ret


def annotate_distance(ax, txt, start, stop):
    """
    Annotates distance
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Current axes
    txt: string
        Annotated text
    start: float array
        Start point (x,y)
    stop: float array
        Stop point (x,y)
    """
    ax.annotate('', xy=start, xycoords='data', xytext=stop, textcoords='data',
                arrowprops={'arrowstyle': '|-|,widthA=0.25,widthB=0.25'})
    ax.annotate(txt, xy=((start[0] + stop[0]) / 2, (start[1] + stop[1]) / 2), xycoords='data',
                xytext=(0, -2), textcoords='offset points', horizontalalignment='center', verticalalignment='top',
                bbox=wbbox)


# Grid
def grid(ax):
    """
    Grid, but below axis
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Current axes
    """
    ax.grid()
    ax.set_axisbelow(True)


def update_xlim(ax, x, dx, xmax=5):
    ax.set_xlim([np.max([np.min(x), -xmax]) - dx, np.min([np.max(x), xmax]) + dx])


def update_ylim(ax, y, dy, ymax=5):
    ax.set_ylim([np.max([np.min(y), -ymax]) - dy, np.min([np.max(y), ymax]) + dy])


# Default figure sizes
fig_width = 10
fig_aspect = 16/9
landscape = {'figsize': (fig_width, fig_width/fig_aspect)}

# Styles
style_poles = {'color': 'rwth:blue', 'marker': 'x', 'mew': 2, 'ms': 5.5, 'ls': 'None'}
style_zeros = {'color': 'rwth:blue', 'marker': 'o', 'mew': 2, 'ms': 5.5, 'mfc': 'None', 'ls': 'None'}
style_graph = {'color': 'rwth:blue'}

# Widget label style (full width)
wdgtl_style = {'description_width': 'initial'}

# Axis white background
wbbox = {"facecolor": "white", "edgecolor": "None", "pad": 0}

# Propagate rwth_colors to default matplotlib colors
mcolors.get_named_colors_mapping().update(colors.rwth_colors)


# Custom stem function
def stem(ax, x, y, color='rwth:blue', **kwargs):
    container = ax.stem(x, y, use_line_collection=True, basefmt=" ", **kwargs)
    plt.setp(container, 'Color', color)
    return container


def stem_set_data(container, x, y):
    tmp = [np.array([[xt, 0], [xt, yt]]) for xt, yt in zip(x, y)]
    container[1].set_segments(tmp)
    container[0].set_data(x, y)


def stem_set_xdata(container, x):
    y = container[0].get_ydata()
    stem_set_data(container, x, y)


def stem_set_ydata(container, y):
    x = container[0].get_xdata()
    stem_set_data(container, x, y)


# Custom dirac plot
def plot_dirac(ax, x, y, color='rwth:blue', **kwargs):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = y >= 0
    xp = x[mask]
    yp = y[mask]
    if not len(xp):
        xp = np.nan*np.ones(2); yp=xp
    cp = stem(ax, xp, yp, color, markerfmt="^", **kwargs)
    
    mask = y < 0
    xn = x[mask]
    yn = y[mask]
    kwargs.pop('label', None)  # one legend label is enough

    if not len(xn):
        xn = np.nan*np.ones(2); yn=xn
    
    cn = stem(ax, xn, yn, color, markerfmt="v", **kwargs)
    
    return cp, cn


def dirac_set_data(containers, x, y):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = y >= 0
    xp = x[mask]
    yp = y[mask]
    if len(xp):
        stem_set_data(containers[0], xp, yp)
    else:
        stem_set_data(containers[0], [], [])

    mask = y < 0
    xn = x[mask]
    yn = y[mask]
    if len(xn):
        stem_set_data(containers[1], xn, yn)
    else:
        stem_set_data(containers[1], [], [])


def dirac_weights(ax, x, y, weights, **kwargs):
    x = np.asarray(x)[np.newaxis]
    y = np.asarray(y)[np.newaxis]
    weights = np.asarray(weights)[np.newaxis]
    for xt, yt, weight in zip(x, y, weights):
        if weight != 1:
            ax.text(xt, yt, '(' + str(weight) + ')', **kwargs)


# Laplace Region of Convergence
def plot_lroc(ax, roc, xmax=12, ymax=12):
    y1 = [-ymax, -ymax]
    y2 = [ymax, ymax]

    mask = np.isinf(roc)
    roc[mask] = np.sign(roc[mask]) * xmax
    lleft, = ax.plot([roc[0], roc[0]], [y1[0], y2[0]], ls="--", c="rwth:blue-50")
    lright, = ax.plot([roc[1], roc[1]], [y1[0], y2[0]], ls="--", c="rwth:blue-50")
    hatch = ax.fill_between(roc, y1, y2, facecolor="none", hatch="\\", edgecolor="rwth:blue-50", linewidth=0.0)

    return [lleft, lright, hatch]

def update_lroc(ax, plot, roc, xmax=12, ymax=12):
    y1 = [-ymax, -ymax]
    y2 = [ymax, ymax]

    mask = np.isinf(roc)
    roc[mask] = np.sign(roc[mask]) * xmax

    plot[0].set_xdata([roc[0], roc[0]])
    plot[1].set_xdata([roc[1], roc[1]])
    plot[2].remove()
    plot[2] = ax.fill_between(roc, y1, y2, facecolor="none", hatch="\\", edgecolor="rwth:blue-50",
                                             linewidth=0.0)

    return plot

# z Region of Convergence
def plot_zroc(ax, roc, rmax=12):
    from matplotlib.patches import Circle
    mask = np.isinf(roc)
    roc[mask] = np.sign(roc[mask]) * rmax

    # plot circles
    unitcircle = Circle((0, 0), radius=1, edgecolor="k", fill=False, linestyle='-')
    ax.add_artist(unitcircle)

    theta = np.linspace(0, 2 * np.pi, 1001)
    xs = np.outer(np.abs(roc), np.cos(theta))
    ys = np.outer(np.abs(roc), np.sin(theta))
    xs[1, :] = xs[1, ::-1]
    ys[1, :] = ys[1, ::-1]

    return ax.fill(np.ravel(xs), np.ravel(ys), facecolor="none", hatch="\\", edgecolor="rwth:blue-50", linestyle='--')[0]


def annotate_order(ax, p, ord):
    for index, order in enumerate(ord):
        if order > 1:
            ax.text(np.real(p[index]), np.imag(p[index]), '(' + str(order) + ')', color='black')
            ax.text(np.real(p[index]), -np.imag(p[index]), '(' + str(order) + ')', color='black')

