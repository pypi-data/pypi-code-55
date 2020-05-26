"""
Core plotting tools for tfields library. Especially PlotOptions class
is basis for many plotting expansions

TODO:
    * add other library backends. Do not restrict to mpl
"""
import warnings
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from six import string_types


def set_default(dictionary, attr, value):
    """
    Set defaults to a dictionary
    """
    if attr not in dictionary:
        dictionary[attr] = value


class PlotManager(object):
    """
    processing kwargs for plotting functions and providing easy
    access to axes, dimension and plotting method as well as indices
    for array choice (x..., y..., z_index)

    Examples:
        >>> import rna

        Dimension arguemnt (dim)
        >>> rna.plotting.use('matplotlib')  # which is default anyway
        >>> pm = rna.plotting.PlotManager({})
        >>> pm.dim
        2
        >>> rna.plotting.axes_dim(pm.axes)
        2

        >>> pm = rna.plotting.PlotManager({'dim': 3})
        >>> pm.dim
        3
        >>> rna.plotting.axes_dim(pm.axes)
        3

        >>> rna.plotting.use('pyqtgraph')
        >>> pm = rna.plotting.PlotManager({})
        >>> pm.dim
        3
        >>> rna.plotting.axes_dim(pm.axes)
        3

        Passing an axes object specifically
        >>> rna.plotting.use('matplotlib')
        >>> axes = rna.plotting.gca(3)
        >>> pm = rna.plotting.PlotManager({'axes': axes})

    """
    axes_default = None
    dim_default = None
    x_index_default = 0
    y_index_default = 1
    z_index_default = None
    method_default = None
    def __init__(self, kwargs):
        kwargs = dict(kwargs)

        # axes are generated with priority of kwargs as 'axes', 'dim', 'z_index'
        self._axes = kwargs.pop('axes', self.axes_default)
        self._dim = kwargs.pop('dim', self.dim_default)
        self._x_index = kwargs.pop('x_index', self.x_index_default)
        self._y_index = kwargs.pop('y_index', self.y_index_default)
        self._z_index = kwargs.pop('z_index', self.z_index_default)
        if self.axes is None:
            # if self.dim is None:
            #     if self._z_index is None:
            #         self.dim = 2
            #     else:
            #         self.dim = 3
            
            # set default axes defined by backend method 'gca'
            import rna.plotting
            self.axes = rna.plotting.gca(self._dim)
        self.method = kwargs.pop('method', self.method_default)

        self.plot_kwargs = kwargs

    @property
    def method(self):
        """
        Method for plotting. Will be callable together with plot_kwargs
        """
        return self._method

    @method.setter
    def method(self, method):
        if not isinstance(method, str):
            self._method = method
        else:
            self._method = getattr(self.axes, method)

    @property
    def dim(self):
        """
        axes dimension. If not axes object is given, the dimension defaults to 2
        unless z_index is given which means dim=3
        Examples:
            >>> import rna

            >>> kwargs = dict(dim=3)
            >>> pm = rna.plotting.PlotManager(kwargs)
            >>> rna.plotting.axes_dim(pm.axes)
            3

            >>> kwargs = dict(z_index=42)
            >>> pm = rna.plotting.PlotManager(kwargs)
            >>> rna.plotting.axes_dim(pm.axes)
            3

        """
        return self._dim

    @dim.setter
    def dim(self, dim):
        if dim != self._dim:
            # explicit call to change dimension and thus also change axes
            # do not raise warning
            self._dim = dim
            self._z_index = None
            import rna.plotting
            self.axes = rna.plotting.gca(dim)

        # check and set z_index
        if dim == 2:
            if self._z_index is not None:
                warnings.warn("Dimension is set to 2 but z_index is not None")
            self._z_index = None
        elif dim == 3:
            if self._z_index is None:
                # auto compute the z_index if axes dim is 3
                indices_used = [0, 1, 2]
                indices_used.remove(self._x_index)
                indices_used.remove(self._y_index)
                z_index = indices_used[0]
                self._z_index = z_index
        else:
            raise NotImplementedError("Dimensions other than 2 or 3 are not supported.")
        self._dim = dim

    @property
    def axes(self):
        """
        The Axes object that belongs to this instance
        """
        return self._axes

    @axes.setter
    def axes(self, axes):
        self._axes = axes
        
        # correct dimensions if necessary
        from rna.plotting import axes_dim
        dim = axes_dim(self._axes)
        if self.dim is not None and self.dim != dim:
            warnings.warn("Axes force dimensions that were set differently before.")
        self.dim = dim

    @property
    def state(self):
        """
        Returns:
            dict: dict which can be used to reconstruct the state of the current
            object

        Examples:
            Setting up a PlotManager
            >>> import rna
            >>> kwargs = {'method': 'plot', 'dim': 2}
            >>> plot_manager = rna.plotting.PlotManager(kwargs)
            >>> rna.plotting.set_default(kwargs, 'method', 'scatter')

            Pass the state arguments to the next PlotManager

            >>> state = plot_manager.state
            >>> plot_manager_2 = rna.plotting.PlotManager(state)
            >>> plot_manager_2.state['method']  # doctest: +ELLIPSIS
            <bound method Axes.plot of <matplotlib.axes._subplots.AxesSubplot object ...>>
            >>> plot_manager_2.state['axes']  # doctest: +ELLIPSIS
            <matplotlib.axes._subplots.AxesSubplot object ...>

            If some argument is None it will be not occuring in the state

            >>> plot_manager.method = None
            >>> assert 'method' not in plot_manager.state
            
        """
        state_dict = dict(self.plot_kwargs)
        for state_key in ['axes', 'x_index', 'y_index', 'z_index', 'dim', 'method']:
            state_value = getattr(self, '_' + state_key)
            state_value_default = getattr(self, state_key + '_default')
            if state_value != state_value_default:
                state_dict[state_key] = state_value
        return state_dict

    def get_axis_indices(self):
        return self._x_index, self._y_index, self._z_index

    def set_vmin_vmax_auto(self, vmin, vmax, scalars):
        """
        Automatically set vmin and vmax as min/max of scalars
        but only if vmin or vmax is None
        """
        if scalars is None:
            return
        if len(scalars) < 2:
            warnings.warn("Need at least two scalars to autoset vmin and/or vmax!")
            return
        if vmin is None:
            vmin = min(scalars)
            self.plot_kwargs['vmin'] = vmin
        if vmax is None:
            vmax = max(scalars)
            self.plot_kwargs['vmax'] = vmax

    def get_norm_args(self, vmin_default=0, vmax_default=1, cmap_default=None):
        """
        Examples:
            >>> import rna
            >>> rna.plotting.set_style()
            >>> pm = rna.plotting.PlotManager(dict(vmin=2, vmax=42))
            >>> pm.get_norm_args()
            ('viridis', 2, 42)
        """
        if cmap_default is None:
            cmap_default = plt.rcParams['image.cmap']
        cmap = self.get('cmap', cmap_default)
        vmin = self.get('vmin', vmin_default)
        vmax = self.get('vmax', vmax_default)
        if vmin is None:
            vmin = vmin_default
        if vmax is None:
            vmax = vmax_default
        return cmap, vmin, vmax

    def pop_norm_args(self, **defaults):
        """
        Pop vmin, vmax and cmap from plot_kwargs
        Args:
            **defaults:
                see get_norm_args method
        """
        cmap, vmin, vmax = self.get_norm_args(**defaults)
        self.pop('cmap');
        self.pop('vmin');
        self.pop('vmax')
        return cmap, vmin, vmax

    def format_colors(self, colors, fmt='rgba', length=None):
        """
        format colors according to fmt argument
        Args:
            colors (list/one value of rgba tuples/int/float/str): This argument will
                be interpreted as color
            fmt (str): rgba | hex | norm
            length (int/None): if not None: correct colors lenght
    
        Returns:
            colors in fmt
        """
        cmap, vmin, vmax = self.get_norm_args(cmap_default='viridis',
                                              vmin_default=None,
                                              vmax_default=None)
        from rna.plotting.colors import to_colors
        return to_colors(colors, fmt, length=length,
                         vmin=vmin, vmax=vmax, cmap=cmap)

    def sort_labels(self, labels):
        """
        Returns the labels corresponding to the axis_indices
        """
        return [labels[i] for i in self.get_axis_indices() if i is not None]
        
    def get(self, attr, default=None):
        return self.plot_kwargs.get(attr, default)

    def pop(self, attr, default=None):
        return self.plot_kwargs.pop(attr, default)

    def set(self, attr, value):
        self.plot_kwargs[attr] = value

    def set_default(self, attr, value):
        set_default(self.plot_kwargs, attr, value)

    def retrieve(self, attr, default=None, keep=True):
        if keep:
            return self.get(attr, default)
        else:
            return self.pop(attr, default)

    def retrieve_chain(self, *args, **kwargs):
        default = kwargs.pop('default', None)
        keep = kwargs.pop('keep', True)
        if len(args) > 1:
            return self.retrieve(args[0],
                                 self.retrieve_chain(*args[1:],
                                                    default=default,
                                                    keep=keep),
                                 keep=keep)
        if len(args) != 1:
            raise ValueError("Invalid number of args ({0})".format(len(args)))
        return self.retrieve(args[0], default, keep=keep)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # doctest.run_docstring_examples(as_tensors_list, globals())
