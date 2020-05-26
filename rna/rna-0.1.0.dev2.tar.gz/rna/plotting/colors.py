"""
Color conversion
"""
from six import string_types
from itertools import cycle
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


FMT_LENGTHS = {
    'str': None,
    'norm': None,
    'rgba': 4,
    'rgb': 3,
    'hex': None,
}


def color_fmt(colors):
    """
    Determine the color representation of
    Args:
        colors (various)
    Returns:
        str: color representation type ('str', 'norm', 'rgba', 'rgb')
            returns None if fmt unknown
    """
    if not hasattr(colors, '__iter__') or isinstance(colors, string_types):
        # colors is just one element
        colors = [colors]
    color = colors[0]

    if isinstance(color, string_types):
        return 'str'
    if isinstance(color, (int, float, np.float32, np.float64, np.integer)):
        return 'norm'
    if isinstance(color, tuple):
        if len(color) == FMT_LENGTHS['rgba']:
            return 'rgba'
        if len(color) == FMT_LENGTHS['rgb']:
            return 'rgb'
    return None


def truncate_colormap(cmap, vmin=0.0, vmax=1.0, n=100):
    cmap = plt.get_cmap(cmap)
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=vmin, b=vmax),
        cmap(np.linspace(vmin, vmax, n)))
    return new_cmap


def to_colors(colors, fmt='rgba', length=None,
              vmin=None, vmax=None, cmap=None):
    """
    format colors according to fmt argument
    Args:
        colors (list/one value of rgba tuples/int/float/str):
            This argument will be interpreted as color
        fmt (str): rgba | rgb | hex | norm
        length (int/None): if not None: correct colors lenght

    Returns:
        colors in fmt

    Examples:
        >>> import rna
        >>> import numpy as np
        >>> rna.plotting.colors.to_colors(1, cmap='gray', vmin=0)
        array([ 1.,  1.,  1.,  1.])
        >>> rna.plotting.colors.to_colors(1, length=2, cmap='gray', vmin=0)
        array([[ 1.,  1.,  1.,  1.],
               [ 1.,  1.,  1.,  1.]])
        >>> rna.plotting.colors.to_colors([1], cmap='gray', vmin=0)
        array([[ 1.,  1.,  1.,  1.]])

        Keeps the shape
        >>> rna.plotting.colors.to_colors(np.array([[1,1],[1,1]]), cmap='gray', vmin=0)
        array([[[ 1.,  1.,  1.,  1.],
                [ 1.,  1.,  1.,  1.]],
        <BLANKLINE>
               [[ 1.,  1.,  1.,  1.],
                [ 1.,  1.,  1.,  1.]]])

    """
    has_iter = True
    if not hasattr(colors, '__iter__') or isinstance(colors, string_types):
        # colors is just one element
        has_iter = False
        colors = [colors]

    # work on a flat color array and reshape afterwards
    colors = np.array(colors)
    shape = list(colors.shape)
    colors = np.array(colors.flat)

    orig_fmt = color_fmt(colors[0])

    if orig_fmt == 'norm' or fmt == 'norm':
        if orig_fmt == 'norm':
            if cmap is None:
                raise TypeError("norm conversion always requires cmap")
            # from IPython import embed; embed()
            if vmin is None:
                vmin = min(colors)
            if vmax is None:
                vmax = max(colors)
        else:
            if vmin is None or vmax is None or cmap is None:
                raise TypeError("norm conversion always requires cmap, "
                                "vmin and vmax.")
    # already correct
    if orig_fmt == fmt:
        pass
    elif fmt == 'norm':
        colors_rgba = to_colors(colors, 'rgba')
        colors = rgba_to_norm(colors_rgba, cmap, vmin, vmax)
    elif fmt == 'rgba':
        if orig_fmt == 'str':
            colors = [mpl.colors.to_rgba(color) for color in colors]
        elif orig_fmt == 'rgb':
            warnings.warn("Assuming alpha of 1")
            colors = [c + (1,) for c in colors]
        elif orig_fmt == 'norm':
            colors = norm_to_rgba(colors,
                                  vmin=vmin,
                                  vmax=vmax,
                                  cmap=cmap)
        else:
            raise NotImplementedError()
    elif fmt == 'hex':
        colors_rgva = to_colors(colors, 'rgba')
        colors = [mpl.colors.to_hex(color) for color in colors_rgva]
    else:
        raise NotImplementedError("Color fmt '{fmt}' not implemented."
                                  .format(**locals()))

    if length is not None:
        # just one colors value given
        if len(colors) != length:
            if not len(colors) == 1:
                raise ValueError("Can not correct color length")
            colors = np.repeat(colors, length)
            shape[0] = length
            # colors = list(colors)
            # colors *= length
    elif not has_iter:
        shape = shape[1:]
        colors = colors[0]

    colors = np.array(colors)

    # correct the shape for the new length of the fmt
    if FMT_LENGTHS[orig_fmt] is not FMT_LENGTHS[fmt]:
        if FMT_LENGTHS[orig_fmt] is None:
            shape += [FMT_LENGTHS[fmt]]
        elif FMT_LENGTHS[fmt] is None:
            shape = shape[:-1]
        else:
            shape[-1] = FMT_LENGTHS[fmt]

    shape = tuple(shape)
    colors = colors.reshape(shape)
    return colors


def norm_to_rgba(scalars, cmap=None, vmin=None, vmax=None):
    """
    retrieve the rgba colors for a list of scalars

    Examples:
        >>> import rna
        >>> colors = rna.plotting.colors.norm_to_rgba([0, 1, 1.5, 2, 3, 4], vmin=1, vmax=2)
        >>> colors = colors[:, :3]  # strip a for test
        >>> assert all(colors[0] == colors[1])
        >>> assert all(colors[1] != colors[2])
        >>> assert all(colors[2] != colors[3])
        >>> assert all(colors[3] == colors[4])
        >>> assert all(colors[4] == colors[5])

    """
    color_map = plt.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    colors = color_map([norm(s) for s in scalars])
    return colors


def rgba_to_norm(colors, cmap, vmin, vmax):
    """
    Inverse 'norm_to_rgba'
    Reconstruct the numeric values (0 - 1) of given
    Args:
        colors (list or rgba tuple)
        cmap (matplotlib colormap)
        vmin (float)
        vmax (float)
    """
    # colors = np.array(colors)/255.
    rnge = np.linspace(vmin, vmax, 256)
    norm = mpl.colors.Normalize(vmin, vmax)
    mapvals = cmap(norm(rnge))[:, :4]  # there are 4 channels: r,g,b,a
    scalars = []
    for color in colors:
        distance = np.sum((mapvals - color) ** 2, axis=1)
        scalars.append(rnge[np.argmin(distance)])
    return scalars


def colormap(seq):
    """
    Args:
        seq (iterable): a sequence of floats and RGB-tuples.
            The floats should be increasing and in the interval (0,1).
    Returns:
        LinearSegmentedColormap
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)


def color_cycle(cmap=None, n=None):
    """
    Args:
        cmap (matplotlib colormap): e.g. plt.cm.coolwarm
        n (int): needed for cmap argument
    """
    if cmap:
        color_rgb = to_colors(np.linspace(0, 1, n), cmap=cmap, vmin=0, vmax=1)
        colors = map(lambda rgb: '#%02x%02x%02x' % (int(rgb[0] * 255),
                                                    int(rgb[1] * 255),
                                                    int(rgb[2] * 255)),
                     tuple(color_rgb[:, 0:-1]))
    else:
        colors = list([color['color'] for color in mpl.rcParams['axes.prop_cycle']])
    return cycle(colors)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
