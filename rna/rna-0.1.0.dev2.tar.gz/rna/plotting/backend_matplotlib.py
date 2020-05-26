"""
Matplotlib specific plotting
"""
import rna

import numpy as np
import re
import warnings
import os
import matplotlib as mpl
import matplotlib.ticker
from matplotlib import style
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d as plt3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as dates
from matplotlib.patches import Rectangle
import matplotlib.animation as manimation
from contextlib import contextmanager
from itertools import cycle
from functools import partial
import logging


def show():
    plt.show()


def gca(dim=None, **kwargs):
    """
    Forwarding to plt.gca but translating the dimension to projection
    correct dimension
    """
    orig_axes = plt.gca(**kwargs)
    orig_dim = rna.plotting.axes_dim(orig_axes)
    if dim is None:
        axes = orig_axes
    else:
        if dim == orig_dim:
            axes = orig_axes
        elif dim == 3:
            axes = plt.gca(projection='3d', **kwargs)
        elif dim == 2:
            warnings.warn("You have another dimension set as gca."
                          "I will force the new dimension to return.")
            axes = plt.gcf().add_subplot(1, 1, 1, **kwargs)
    return axes


def clear(axes):
    axes.clear()


def upgrade_style(style, source, dest=None):
    """
    Copy a style file at <origionalFilePath> to the <dest> which is the foreseen
    local matplotlib rc dir by default
    The style will be name <style>.mplstyle
    Args:
        style (str): name of style
        source (str): full path to mplstyle file to use
        dest (str): local directory to copy the file to. Matpotlib has to
            search this directory for mplstyle files!
    Examples:
        >>> import rna
        >>> import os
        >>> rna.plotting.use('matplotlib')
        >>> rna.plotting._backend_mod.upgrade_style(
        ...     'tfields',
        ...     os.path.join(os.path.dirname(rna.plotting.__file__),
        ...                  'mplstyles/rna.mplstyle'))

    """
    if dest is None:
        dest = mpl.get_configdir()
    style_extension = 'mplstyle'
    path = rna.path.resolve(os.path.join(dest, style + '.' +
                                                   style_extension))
    source = rna.path.resolve(source)
    rna.path.cp(source, path)


def set_style(style='rna', dest=None, upgrade=False):
    """
    Set the matplotlib style of name
    Important:
        Either you
    Args:
        style (str)
        dest (str): local directory to use file from. if None, use default
            maplotlib destination
    """
    if dest is None:
        dest = mpl.get_configdir()

    style_extension = 'mplstyle'
    path = rna.path.resolve(os.path.join(dest, style + '.' + style_extension))
    if style in mpl.style.available and not upgrade:
        plt.style.use(style)
    elif os.path.exists(path) and not upgrade:
        plt.style.use(path)
    else:
        log = logging.getLogger()
        source = rna.path.resolve(
            os.path.join(
                os.path.join(os.path.dirname(__file__), 'mplstyles'),
                style + '.' + style_extension))
        if os.path.exists(source):
            log.warning("I will copy the style {style} to {dest}."
                        .format(**locals()))
            try:
                upgrade_style(style, source, dest)                
                set_style(style)
            except Exception:
                log.error("Could not set style")
        else:
            log.error("Could not set style {path}. Probably you would want to"
                      "call rna.plotting.upgrade_style(<style>, "
                      "<path to mplstyle file that should be copied>)"
                      "once".format(**locals()))


def _save(path, **kwargs):
    """
    Args:
        path
        **kwargs:
            width (float): figure width in pts.
            scale (float): Fraction of the width which you wish
                the figure to occupy
            ratio (float): height to width ratio
            post_process (bool): switch post-processing of pgfs on and of
            substitutes (list of tuple of str): 
            scaling (str): Default is r"\igraph@width"
            - further are passed to savefig

    """
    # catch figure from axes or fig
    axes = kwargs.get('axes', None)
    if axes is None:
        fig_default = plt.gcf()
        axes = gca()
        if fig_default is None:
            raise ValueError("fig_default may not be None")
    else:
        fig_default = axes.figure
    fig = kwargs.get('fig', fig_default)

    # resize the figure to match a given width (in pt).
    width = kwargs.pop('width', None)
    scale = kwargs.pop('scale', 1.)
    orig_size = fig.get_size_inches()
    orig_ratio = orig_size[1] / orig_size[0]
    ratio = kwargs.pop('ratio', orig_ratio)
    if width is not None:
        fig.set_size_inches(*rna.plotting.figsize(width, scale=scale,
            ratio=ratio))

    # crop the plot down based on the extents of the artists in the plot
    kwargs['bbox_inches'] = kwargs.pop('bbox_inches', 'tight')
    if kwargs['bbox_inches'] == 'tight':
        extra_artists = None
        for ax in fig.get_axes():
            first_label = ax.get_legend_handles_labels()[0] or None
            if first_label:
                if not extra_artists:
                    extra_artists = []
                if isinstance(first_label, list):
                    extra_artists.extend(first_label)
                else:
                    extra_artists.append(first_label)
        kwargs['bbox_extra_artists'] = kwargs.pop('bbox_extra_artists',
                                                  extra_artists)

    # pgf post-processing works but matpltolib pgf backend writes pgftext left
    # adjusted and creates right adjusted text by moving the text in x
    # this makes it impossible to rescale text correctly. If one knew, the
    # original was right adjusted a correction could be applied. This way
    # however, we cann not do anything.
    post_process = kwargs.pop('post_process', False)
    pgf_kwargs = {
        'substitutes': kwargs.pop('substitutes', [('\sffamily', '')]),
        'scaling': kwargs.pop('scaling', r"\igraph@width"),
        }


    # set current figure
    plt.figure(fig.number)

    if path.endswith('tikz'):
        import matplotlib2tikz as tikz
        if width is None:
            figurewidth = r"\textwidth"
        else:
            figurewidth = '{0}pt'.format(scale*width)
        tikz.save(path, figurewidth=figurewidth)
    else:
        plt.savefig(path, **kwargs)

    if post_process and path.endswith('pgf'):
        # use it like \igraph[width=0.5\columnwidth]{path_to_the.pgf}
        substitutes = pgf_kwargs.pop('substitutes')
        scaling = pgf_kwargs.pop('scaling')
        with open(path, 'r') as f:
            content = []
            exp = r"(\\pgftext.+)(\\fontsize{.+)\\selectfont(.+)}%"
            exp_width = r"\\pgfpathrectangle{\\pgfpointorigin}{\\pgfqpoint{(.+)}{(.+)}%"
            for line in f:
                res = re.match(exp, line)
                res_width = re.match(exp_width, line)
                if res_width:
                    pgf_path_size = res_width.groups()[0]
                    # factor 72.27 (latex definition differs from pdf # definition) for conversion from in to pt
                    pgf_path_size = r'(' + pgf_path_size.replace('in', '*72.27') + r')'
                if res:
                    groups = res.groups()
                    parts = exp.split(r'(.+)')
                    line = groups[0] + r"\selectfont \scalebox{\fpeval{(%s/(%s))}}{" % (pgf_path_size, scaling)  + groups[2] + r"}}%" + '\n'
                for x, y in substitutes:
                    line = line.replace(x, y)
                content.append(line)
        with open(path, 'w') as f:
            f.writelines(content)

    # reset the figure size
    if width is not None:
        fig.set_size_inches(*orig_size)


def plot_array(array, **kwargs):
    """
    Points3D plotting method.

    Args:
        array (numpy array)
        axes (matplotlib.Axis) object
        x_index (int): coordinate index that should be on x_index
        y_index (int): coordinate index that should be on y_index
        z_index (int or None): coordinate index that should be on z_index.
            If it evaluates to None, 2D plot will be done.
        method (str | callable): method name to use for filling the axes

    Returns:
        Artist or list of Artists (imitating the axes.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    array = np.array(array)
    rna.plotting.set_default(kwargs, 'method', 'scatter')
    plot_manager = rna.plotting.PlotManager(kwargs)

    labels = plot_manager.pop('labels', ['x (m)', 'y (m)', 'z (m)'])
    x_index, y_index, z_index = plot_manager.get_axis_indices()
    set_labels(plot_manager.axes, *plot_manager.sort_labels(labels))
    if z_index is None:
        args = [array[:, x_index],
                array[:, y_index]]
    else:
        args = [array[:, x_index],
                array[:, y_index],
                array[:, z_index]]
    artist = plot_manager.method(*args, **plot_manager.plot_kwargs)
    return artist


def plot_mesh(vertices, faces, **kwargs):
    """
    Args:
        axes (matplotlib axes)
        x_index (int)
        y_index (int)
        z_index (int)
        edgecolor (color)
        color (color): if given, use this color for faces in 2D
        cmap
        vmin
        vmax
    """
    vertices = np.array(vertices)
    faces = np.array(faces)
    if faces.shape[0] == 0:
        warnings.warn("No faces to plot")
        return None
    if max(faces.flat) > vertices.shape[0]:
        raise ValueError("Some faces point to non existing vertices.")
    po = rna.plotting.PlotManager(kwargs)
    if po.dim == 2:
        full = True
        import tfields
        mesh = tfields.Mesh3D(vertices, faces=faces)
        x_index, y_index, z_index = po.get_axis_indices()
        facecolors = po.retrieve_chain('facecolors', 'color',
                                       default=0,
                                       keep=False)
        if full:
            # implementation that will sort the triangles by z_index
            centroids = mesh.centroids()
            axis_indices = [0, 1, 2]
            axis_indices.pop(axis_indices.index(x_index))
            axis_indices.pop(axis_indices.index(y_index))
            z_index = axis_indices[0]
            zs = centroids[:, z_index]
            try:
                iter(facecolors)
                zs, faces, facecolors = tfields.lib.util.multi_sort(
                    zs, faces, facecolors)
            except TypeError:
                zs, faces = tfields.lib.util.multi_sort(zs, faces)

            n_faces_initial = len(faces)
        else:
            # cut away "back sides" implementation
            direction_vector = np.array([1., 1., 1.])
            direction_vector[x_index] = 0.
            direction_vector[y_index] = 0.
            norm_vectors = mesh.triangles().norms()
            dot_product = np.dot(norm_vectors, direction_vector)
            n_faces_initial = len(faces)
            faces = faces[dot_product > 0]

        vertices = mesh

        po.plot_kwargs['method'] = 'tripcolor'
        po.plot_kwargs['triangles'] = faces

        """
        sort out color arguments
        """
        facecolors = po.format_colors(facecolors,
                                      fmt='norm',
                                      length=n_faces_initial)
        if not full:
            facecolors = facecolors[dot_product > 0]
        po.plot_kwargs['facecolors'] = facecolors

        d = po.plot_kwargs
        d['x_index'] = x_index
        d['y_index'] = y_index
        artist = plot_array(vertices, **d)
    elif po.dim == 3:
        label = po.pop('label', None)
        color = po.retrieve_chain('color', 'c', 'facecolors',
                                  default='grey',
                                  keep=False)
        from rna.plotting.colors import color_fmt
        orig_fmt = color_fmt(color)
        orig_color = color
        color = po.format_colors(color,
                                 fmt='rgba',
                                 length=len(faces))
        nanMask = np.isnan(color)
        if nanMask.any():
            warnings.warn("nan found in colors. Removing the corresponding faces!")
            color = color[~nanMask]
            faces = faces[~nanMask]

        edgecolor = po.pop('edgecolor', None)
        alpha = po.pop('alpha', None)
        # delete norm arguments
        po.pop('vmin', None)
        po.pop('vmax', None)
        po.pop('cmap', None)

        triangles = np.array([vertices[face] for face in faces])
        artist = plt3D.art3d.Poly3DCollection(triangles, **po.plot_kwargs)
        po.axes.add_collection3d(artist)

        if edgecolor is not None:
            artist.set_edgecolor(edgecolor)
            artist.set_facecolors(color)
        else:
            artist.set_color(color)
        if orig_fmt == 'norm':
            artist.set_array(np.array(orig_color))  # sets vmin, vmax to min, max of val

        if alpha is not None:
            artist.set_alpha(alpha)

        # for some reason auto-scale does not work
        autoscale_3d(po.axes, array=vertices)

        # legend lables do not work at all as an argument
        if label:
            artist.set_label(label)

        # when plotting the legend edgecolors/facecolors2d are needed
        artist._edgecolors2d = None
        artist._facecolors2d = None

        labels = ['x (m)', 'y (m)', 'z (m)']
        set_labels(po.axes, *po.sort_labels(labels))

    else:
        raise NotImplementedError("Dimension != 2|3")

    return artist


def plot_tensor_field(points, field, **kwargs):
    """
    Args:
        points (array_like): base vectors
        field (): direction field
        **kwargs: passed to PlotManager
    """
    po = rna.plotting.PlotManager(kwargs)
    field = np.array(field)
    if len(field.shape) == 2 and field.shape[1] == 1:
        # scalar
        field = field.reshape(len(points))
    if len(field.shape) == 1:
        # scalar
        colors = po.format_colors(field)
        cmap, vmin, vmax = po.pop_norm_args()
        artists = plot_array(points, color=colors, **po.state)
        if vmin is not None:
            field[np.argwhere(field < vmin)] = vmin
        if vmax is not None:
            field[np.argwhere(field > vmax)] = vmax
        if not isinstance(artists, list):
            artists.set_array(field)
        else:
            raise NotImplementedError("Probably you used plot instead of"
                "scatter. This is not yet implemented because you have n-1"
                "segments but gave n colors.")
    elif len(field.shape) == 2:
        # vector
        if points is None:
            points = np.full(field.shape, 0.)
        x_index, y_index, z_index = po.get_axis_indices()
        artists = []
        for point, vector in zip(points, field):
            if po.dim == 3:
                artists.append(
                    po.axes.quiver(
                        point[x_index], point[y_index], point[z_index],
                        vector[x_index], vector[y_index], vector[z_index],
                        **po.plot_kwargs))
            elif po.dim == 2:
                artists.append(po.axes.quiver(point[x_index], point[y_index],
                                              vector[x_index], vector[y_index],
                                              **po.plot_kwargs))
            else:
                raise NotImplementedError("Dimension != 2|3")
    else:
        raise NotImplementedError("Only Scalars and Vectors implemented")
    return artists


def plot_plane(point, normal, **kwargs):

    def plot_vector(fig, orig, v, color='blue'):
        axes = fig.gca(projection='3d')
        orig = np.array(orig)
        v = np.array(v)
        axes.quiver(orig[0], orig[1], orig[2], v[0], v[1], v[2], color=color)
        axes.set_xlim(0, 10)
        axes.set_ylim(0, 10)
        axes.set_zlim(0, 10)
        axes = fig.gca(projection='3d')
        return fig

    def rotation_matrix(d):
        sin_angle = np.linalg.norm(d)
        if sin_angle == 0:
            return np.identity(3)
        d /= sin_angle
        eye = np.eye(3)
        ddt = np.outer(d, d)
        skew = np.array([[0, d[2], -d[1]],
                         [-d[2], 0, d[0]],
                         [d[1], -d[0], 0]],
                        dtype=np.float64)

        M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
        return M

    def pathpatch_2d_to_3d(pathpatch, z, normal):
        if type(normal) is str:  # Translate strings to normal vectors
            index = "xyz".index(normal)
            normal = np.roll((1.0, 0, 0), index)

        normal /= np.linalg.norm(normal)  # Make sure the vector is normalised
        path = pathpatch.get_path()  # Get the path and the associated transform
        trans = pathpatch.get_patch_transform()

        path = trans.transform_path(path)  # Apply the transform

        pathpatch.__class__ = plt3D.art3d.PathPatch3D  # Change the class
        pathpatch._code3d = path.codes  # Copy the codes
        pathpatch._facecolor3d = pathpatch.get_facecolor  # Get the face color

        verts = path.vertices  # Get the vertices in 2D

        d = np.cross(normal, (0, 0, 1))  # Obtain the rotation vector
        M = rotation_matrix(d)  # Get the rotation matrix

        pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])

    def pathpatch_translate(pathpatch, delta):
        pathpatch._segment3d += delta

    kwargs['alpha'] = kwargs.pop('alpha', 0.5)
    po = rna.plotting.PlotManager(kwargs)
    patch = Circle((0, 0), **po.plot_kwargs)
    po.axes.add_patch(patch)
    pathpatch_2d_to_3d(patch, z=0, normal=normal)
    pathpatch_translate(patch, (point[0], point[1], point[2]))


def plot_sphere(point, radius, **kwargs):
    po = rna.plotting.PlotManager(kwargs)
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = point[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = point[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = point[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    return po.axes.plot_surface(x, y, z, **po.plot_kwargs)


def plot_function(fun, **kwargs):
    """
    Args:
        axes (matplotlib.Axis) object

    Returns:
        Artist or list of Artists (imitating the axes.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    import numpy as np
    labels = ['x', 'f(x)']
    po = rna.plotting.PlotManager(kwargs)
    rna.plotting.set_labels(po.axes, *labels)
    xMin, xMax = po.pop('xMin', 0), po.pop('xMax', 1)
    n = po.pop('n', 100)
    vals = np.linspace(xMin, xMax, n)
    args = (vals, map(fun, vals))
    artist = po.axes.plot(*args,
                          **po.plot_kwargs)
    return artist


def plot_errorbar(points, errors_up, errors_down=None, **kwargs):
    """
    Args:
        axes (matplotlib.Axis) object

    Returns:
        Artist or list of Artists (imitating the axes.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    po = rna.plotting.PlotManager(kwargs)
    po.set_default('marker', '_')

    if errors_down is None:
        errors_down = errors_up

    artists = []

    # plot points
    # artists.append(po.axes.plot(points, **po.plot_kwargs))

    # plot errorbars
    for i in range(len(points)):
        artists.append(
            po.axes.plot([points[i, 0] + errors_up[i, 0],
                          points[i, 0] - errors_down[i, 0]],
                         [points[i, 1], points[i, 1]],
                         [points[i, 2], points[i, 2]],
                         **po.plot_kwargs))
        artists.append(
            po.axes.plot([points[i, 0], points[i, 0]],
                         [points[i, 1] + errors_up[i, 1],
                          points[i, 1] - errors_down[i, 1]],
                         [points[i, 2], points[i, 2]],
                         **po.plot_kwargs))
        artists.append(
            po.axes.plot([points[i, 0], points[i, 0]],
                         [points[i, 1], points[i, 1]],
                         [points[i, 2] + errors_up[i, 2],
                          points[i, 2] - errors_down[i, 2]],
                         **po.plot_kwargs))

    return artists


"""
Display section
"""


def axes_dim(axes):
    """
    Returns int: axes dimension
    """
    if hasattr(axes, 'get_zlim'):
        return 3
    else:
        return 2


def set_aspect_equal(axes):
    """Fix equal aspect bug for 3D plots."""

    if axes_dim(axes) == 2:
        axes.set_aspect('equal')
        return

    xlim = axes.get_xlim3d()
    ylim = axes.get_ylim3d()
    zlim = axes.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    axes.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    axes.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    axes.set_zlim3d([zmean - plot_radius, zmean + plot_radius])


def set_axis_off(axes):
    if axes_dim(axes) == 2:
        axes.set_axis_off()
    else:
        axes._axis3don = False


def autoscale_3d(axes, array=None, xLim=None, yLim=None, zLim=None):
    if array is not None:
        xMin, yMin, zMin = array.min(axis=0)
        xMax, yMax, zMax = array.max(axis=0)
        xLim = (xMin, xMax)
        yLim = (yMin, yMax)
        zLim = (zMin, zMax)
    xLimAxis = axes.get_xlim()
    yLimAxis = axes.get_ylim()
    zLimAxis = axes.get_zlim()

    if not False:
        # not empty axes
        xMin = min(xLimAxis[0], xLim[0])
        yMin = min(yLimAxis[0], yLim[0])
        zMin = min(zLimAxis[0], zLim[0])
        xMax = max(xLimAxis[1], xLim[1])
        yMax = max(yLimAxis[1], yLim[1])
        zMax = max(zLimAxis[1], zLim[1])
    axes.set_xlim([xMin, xMax])
    axes.set_ylim([yMin, yMax])
    axes.set_zlim([zMin, zMax])


def set_legend(axes, artists, **kwargs):
    """
    Convenience method to set a legend from multiple artists to an axes.
    Args:
        **kwargs
            table (bool): if True, labels containing ',' will be mapped to table
            table_title (str): value of the table entry top left - only active
                if table
    Examples:
        >> import rna
        >> import matplotlib.pyplot as plt
        >> import pylab

        >> fig = plt.figure()
        >> ax = fig.add_subplot(111)

        >> im1 = ax.plot(range(10), pylab.randn(10), "r--", label=(r"$i = 1$,$j = 1$"))
        >> im2 = ax.plot(range(10), pylab.randn(10), "g--", label=(r"$i = 1$,$j = 2$"))
        >> im3 = ax.plot(range(10), pylab.randn(10), "b--", label=(r"$i = 1$,$j = 3$"))
        >> im4 = ax.plot(range(10), pylab.randn(10), "r.",  label=(r"$i = 2$,$j = 1$"))
        >> im5 = ax.plot(range(10), pylab.randn(10), "g.",  label=(r"$i = 2$,$j = 2$"))
        >> im6 = ax.plot(range(10), pylab.randn(10), "b.",  label=(r"$i = 2$,$j = 3$"))
        >> im7 = ax.plot(range(10), pylab.randn(10), "r^",  label=(r"$i = 3$,$j = 1$"))
        >> im8 = ax.plot(range(10), pylab.randn(10), "g^",  label=(r"$i = 3$,$j = 2$"))
        >> im9 = ax.plot(range(10), pylab.randn(10), "b^",  label=(r"$i = 3$,$j = 3$"))
        >> handles = [im1, im2, im3, im4, im5, im6, im7, im8, im9]

        >> rna.plotting.set_legend(ax, handles, table=True)

        >> plt.show()
    """
    table = kwargs.pop('table', False)
    labels = kwargs.pop('labels', None)
    ncol = kwargs.pop('ncol', None)

    handles = []
    for artist in artists:
        if isinstance(artist, list):
            handles.append(artist[0])
        elif isinstance(artist, tuple):
            tuple_handle = tuple()
            for sub_artist in artist:
                if isinstance(sub_artist, list):
                    tuple_handle += (sub_artist[0],)
                else:
                    tuple_handle += (sub_artist,)
            handles.append(tuple_handle)
        else:
            handles.append(artist)

    if labels is None and any([isinstance(h, tuple) for h in handles]):
        labels = []
        for h in handles:
            if isinstance(h, tuple):
                sub_labels = [sub_h.get_label() for sub_h in h]
                label = sub_labels[0]
                for sub_label in sub_labels[1:]:
                    if not sub_label.startswith('_'):
                        label += sub_label
            else:
                label = h.get_label()
            labels.append(label)

    if table and labels is None and ncol is None:
        table_title = kwargs.pop('table_title', '')
        labels = np.array([h.get_label() for h in handles])
        labels = [l.split(',') for l in labels]
        captions_i = []
        captions_j = []
        for l in labels:
            if l[0] not in captions_i:
                captions_i.append(l[0])
            if l[1] not in captions_j:
                captions_j.append(l[1])
                
        shape = (len(captions_i),
                 len(captions_j))
        
        # initialize
        shape = np.array(shape)
        handles = np.array(handles)
        
        # create blank rectangle
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        
        # Create organized list containing all handles for table. Extra represent empty space
        handles_table = np.full(shape + 1, extra, dtype=object)
        for handle, label in zip(handles, labels):
            i = captions_i.index(label[0])
            j = captions_j.index(label[1])
            if handles_table[i + 1, j + 1] != extra:
                raise ValueError("Duplicate label {label}"
                                 .format(**locals()))
            handles_table[i + 1, j + 1] = handle

        # Define the label captions
        labels_table = np.full(shape + 1, '', dtype='S80')
        labels_table[0, 0] = table_title
        labels_table[0, 1:] = captions_j
        labels_table[1:, 0] = captions_i
        labels_table = labels_table.astype(str)
        
        handles = list(handles_table.flat)
        labels = list(labels_table.flat)
        kwargs['ncol'] = shape[0] + 1
        kwargs['handletextpad'] = kwargs.pop('handletextpad', -1.5)  # negative numbers move to the right
        kwargs['columnspacing'] = kwargs.pop('columnspacing', 1.5)

    return axes.legend(handles=handles, labels=labels, **kwargs)


class set_zoomable(object):
    """
    Left click a colorbar and release in order to zoom.
    Upper and lower 5% of the colorbar will zoom out.
    """
    def __init__(self, cbar):
        self._cbar = cbar
        self._v_press = None
        self._v_release = None

        artist = self._cbar.mappable
        self._press_connection_id = artist.axes.figure.canvas.mpl_connect(
            'button_press_event',
            partial(self.on_press))
        self._release_connection_id = artist.axes.figure.canvas.mpl_connect(
            'button_release_event',
            partial(self.on_release))

    def on_press(self, event):
        if event.inaxes is self._cbar.ax:
            self._v_press = event.ydata

    def on_release(self, event):
        if event.inaxes is self._cbar.ax:
            self._v_release = event.ydata
            self.update_v_min_max()

    def update_v_min_max(self):
        # sort press and release event
        if self._v_press > self._v_release:
            x_up = self._v_press
            x_low = self._v_release
        if self._v_press < self._v_release:
            x_up = self._v_release
            x_low = self._v_press

        # zoom out if in 5% margin
        if x_up > 0.95:
            x_up = 1.5
        if x_low < 0.05:
            x_low = -0.5

        artist = self._cbar.mappable
        vmin, vmax = artist.get_clim()
        v_range = vmax - vmin
        vmax = vmin + x_up * v_range
        vmin = vmin + x_low * v_range
        artist.set_clim(vmin, vmax)
        artist.axes.figure.canvas.draw()


def set_colorbar(axes, artist, label=None, divide=True,
                 position='right', size="2%", pad=0.05,
                 labelpad = None, zoom=False,
                 **kwargs):
    """
    Note:
        Bug found in matplotlib:
            when calling axes.clear(), the colorbar has to be removed by hand,
            since it will not be removed by clear.
        >> import rna
        >> axes = rna.plotting.gca()
        >> artist = ...
        >> cbar = rna.plotting.set_colorbar(axes, artist)
        >> rna.plotting.save(...)
        >> cbar.remove()  # THIS IS IMPORTANT. Otherwise you will have problems
        # at the next call of savefig.
        >> axes.clear()

    """
    ticks_position = 'default'
    label_position = 'bottom'
    labelpad = 30 if labelpad is None else labelpad
    if position == 'right':
        rotation = 270
    elif position == 'left':
        rotation = 90
    elif position == 'top':
        rotation = 0
        ticks_position = 'top'
        label_position = 'top'
        labelpad = 5
    elif position == 'bottom':
        rotation = 0
    # colorbar
    if divide and axes_dim(axes) == 2:
        divider = make_axes_locatable(axes)
        axes = divider.append_axes(position, size=size, pad=pad)
        cbar = plt.colorbar(artist, cax=axes, **kwargs)
    else:
        cbar = plt.colorbar(artist, ax=axes, **kwargs)
    cbar.ax.xaxis.set_ticks_position(ticks_position)
    cbar.ax.xaxis.set_label_position(label_position)
    cbar.ax.tick_params(axis='x', which='major', pad=0)

    # label
    if label is None:
        art_label = artist.get_label()
        if art_label:
            label = art_label
    if label is not None:
        cbar.set_label(label, rotation=rotation, labelpad=labelpad)

    if zoom:
        set_zoomable(cbar)

    return cbar


def set_labels(axes, *labels):
    """
    Set x, y and possibly z labels
    """
    axes.set_xlabel(labels[0])
    axes.set_ylabel(labels[1])
    if axes_dim(axes) == 3:
        axes.set_zlabel(labels[2])
    elif axes_dim(axes) != 2:
        raise ValueError("Axis dimensions other than 2 or 3 is not supported"
                         "for set_labels.")


def set_formatter(sub_axes=None, formatter=dates.DateFormatter('%d-%m-%y')):
    if sub_axes is None:
        axes = gca()
        sub_axes = axes.xaxis
    sub_axes.set_major_formatter(formatter)


class ScientificFormatter(mpl.ticker.ScalarFormatter):
    """
    Examples:
        >> cbar = rna.plotting.set_colorbar(
        ..     axes, artist,
        ..     label=r"$q_c\;(MW/m^2)$",
        ..     format=rna.plotting.backend.ScientificFormatter(None, useMathText=False))
    Args:
        oom (int): order of magnitued on the axes
        **kwargs: forwarded to ScalarFormatter
    """
    def __init__(self, oom=None, **kwargs):
        self._oom = oom
        super(ScientificFormatter, self).__init__(**kwargs)

    def _set_orderOfMagnitude(self, oom):
        self._exp = int(np.log10(oom))
        if self._oom is not None:
            oom = self._oom
        else:  # Default: -3, 0, 3, 6, ...
            oom = self._exp - (self._exp % 3)
        self.orderOfMagnitude = oom


#### ANIMATION

try:
    FFMPEGWRITER = manimation.writers['ffmpeg']
    FFMPEG = True
except Exception as err:
    logging.getLogger().warning(err.message)
    FFMPEGWRITER = object
    FFMPEG = False


class Writer(FFMPEGWRITER):
    """
    FFMPEGWRITER child
    Args:
        **kwargs:
            title (str)
            comment (str)
            fps (int)

    Examples:
        >>> import numpy as np
        >>> import rna
        >>> axes = rna.plotting.gca()
        >>> writer = rna.plotting._backend_mod.Writer()
        >>> pictures = np.array([[[1,1], [0,0]],
        ...                      [[0.5,1], [0,0.5]]])
        >>> with writer.saving():
        ...     for s in pictures:
        ...         artist = axes.imshow(s.T)
        ...         writer.grab_frame()
        ...         axes.clear()
    """
    def __init__(self, **kwargs):
        if FFMPEG:
            # set Defaults
            title = kwargs.pop("title", "")
            comment = kwargs.pop("comment", "")
            artist = kwargs.pop('artist', 'rna plotting module')
            fps = kwargs.pop("fps", 15)
            if len(kwargs) > 0:
                raise ValueError("Some Attributes are not used.")

            # set up writer
            metadata = dict(title=title,
                            artist=artist,
                            comment=comment)
            super(Writer, self).__init__(fps=fps, metadata=metadata)

    @contextmanager
    def saving(self, fig=None, path=None, dpi=300, **kwargs):
        """
        Overwritinig to FFMPEGWRITER.saving
        setting defaults though
        """
        log = logging.getLogger()
        if FFMPEG:
            if fig is None:
                fig = plt.gcf()
            if path is None:
                path = "/tmp/lastMovie.mp4"
            else:
                path = rna.path.resolve(path)
            log.info("Write movie to {path}".format(**locals()))
            with super(Writer, self).saving(fig, path, dpi, **kwargs):
                yield
        else:
            log.warn("FFMPEG Writer not available. Nothing is written!")


if __name__ == '__main__':
    m = tfields.Mesh3D.grid((0, 2, 2), (0, 1, 3), (0, 0, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art1 = m.plot(dim=3, map_index=0, label='twenty')

    m = tfields.Mesh3D.grid((4, 7, 2), (3, 5, 3), (2, 2, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art = m.plot(dim=3, map_index=0, edgecolor='k', vmin=-1, vmax=1, label="something")

    plot_sphere([7, 0, 1], 3)
