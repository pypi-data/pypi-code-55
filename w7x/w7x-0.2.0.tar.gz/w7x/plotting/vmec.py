import w7x
import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def plot_fourier(fourier, **kwargs):
    """Plot fourier coefficients.

    Args:
        fourier (w7x.vmec.FourierCoefficients): fourier coefficients to plot.

    Returns:
        matplotlib.axes: axes.
    """

    num_radial_points = fourier.numRadialPoints
    vmin = kwargs.pop('vmin', 1e-6)
    vmax = kwargs.pop('vmax', 1)
    cax = kwargs.pop('cax', None)
    orientation = kwargs.pop('orientation', 'horizontal')

    #  TODO(@amerlo): Index coefficiets based on radial location
    if num_radial_points != 1:
        raise RuntimeError(
            "Plot for {n} is not implemented yet".format(n=num_radial_points))

    ax = kwargs.pop('axes', None)
    shape = (len(fourier.poloidalModeNumbers),
             len(fourier.toroidalModeNumbers))
    coeffs = np.reshape(fourier.coefficients, shape)

    img = ax.imshow(np.absolute(coeffs),
                    origin='lower',
                    norm=LogNorm(vmin=vmin, vmax=vmax),
                    cmap=plt.get_cmap('YlGnBu_r'))

    if cax is not None:
        plt.colorbar(img, cax=cax, orientation=orientation)

    ax.set_yticks(fourier.poloidalModeNumbers)
    ax.set_xticks(np.arange(0, len(fourier.toroidalModeNumbers)))
    ax.set_xticklabels(fourier.toroidalModeNumbers)
    ax.set_yticklabels(fourier.poloidalModeNumbers)

    return ax


def plot_surface(surface, phi, scalar=None, **kwargs):
    """Plot fourier surface.

    Args:
        surface (w7x.vmec.SurfaceCoefficients): surface object to plot.
        phi (float): toroidal angle to plot in rad.
        scalar (w7x.vmec.FourierCoefficients): scalar values to plot on top.

    Returns:
        matplotlib.axes: axes.
    """

    surface_radial_points = surface.RCos.numRadialPoints

    ax = kwargs.pop('axes', None)
    levels = kwargs.pop('levels', 20)
    cmap = kwargs.pop('cmap', 'RdBu_r')

    num_radial_points = kwargs.pop('nRad', 10)
    num_poloidal_points = kwargs.pop('mPol', 36)
    poloidal_grid = np.linspace(0, 2 * np.pi, num_poloidal_points)

    if surface_radial_points < num_radial_points:
        num_radial_points = surface_radial_points

    component = kwargs.pop('component', None)

    r = []
    z = []
    values = []

    for s in np.linspace(1, surface_radial_points - 1,
                         num_radial_points,
                         dtype=int):
        r.extend(list(surface(s, phi, poloidal_grid)[0]))
        z.extend(list(surface(s, phi, poloidal_grid)[1]))

        if scalar is not None:
            values.extend(list(scalar(s, phi, poloidal_grid, component)))

    if scalar is not None:
        tricnt = ax.tricontourf(r, z, values, levels=levels, cmap=cmap)
        plt.colorbar(tricnt, ax=ax)

    ax.plot(r, z, **kwargs)

    return ax


def _plot_vmec_coil_currents(data, **kwargs):
    """Generate axis for coil currents plot.

    Args:
        data (pandas.DataFrame): data to plot.
        kwargs: Options to pass to matplotlib plotting method.

    Returns:
        matplotlib.axes.Axes: numpy.ndarray of axis, one for each
        coil current to plot.
    """

    _cols = 3
    _rows = 3

    coil_currents_number = len(data.iloc[0])
    currents = ['i1', 'i2', 'i3', 'i4', 'i5', 'iA', 'iB']

    # @amerlo: Because pandas is used only here I do not (yet) want to depend on
    # it. I want to keep w7x slim for deployment. Thus I put the import here.
    import pandas as pd
    df = pd.DataFrame(data.values.tolist(), columns=currents, index=data.index)

    _, axs = plt.subplots(_rows, _cols, constrained_layout=True, **kwargs)
    for ax, current in zip(axs.flat, currents):
        ax.set_title(current)
        df[current].plot(kind='hist', ax=ax)

    return axs


def _plot_vmec_profile(data):
    """Plot vmec profile.

    Args:
        data (pandas.DataFrame): data to plot.

    Returns:
        matplotlib.axes.Axes: matplotlib axes.
    """

    number_radial_points = len(data.iloc[0])
    s = np.linspace(0.0, 1.0, number_radial_points)

    return [plt.plot(s, profile) for _, profile in data.items()]


def plot_vmec(data, feature, **kwargs):
    """Plot vmec runs data.

    Args:
        data (pandas.DataFrame): data to plot.
        feature (String): data column to plot.
        kwargs: Options to pass to matplotlib plotting method.

    Returns:
        matplotlib.axes.Axes: matplotlib axis.
    """

    _profiles = ["pressure", "iota", "toroidalCurrent"]

    if feature == 'coilCurrents':
        return _plot_vmec_coil_currents(data[feature], **kwargs)
    elif feature in _profiles:
        return _plot_vmec_profile(data[feature])
    else:
        return data[feature].plot(kind='hist', **kwargs)
