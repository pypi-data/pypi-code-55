from . import Module, Container
from .activations import Identity
from .im2col import im2col_indices, col2im_indices
import numpy as np


class Linear(Module):
    """
    Implementation of a fully connected layer.

    Attributes
    ----------
    in_features : int
        Number of input features (D) this layer expects.
    out_features : int
        Number of output features (K) this layer expects.
    use_bias : bool
        Flag to indicate whether the bias parameters are used.

    w : Parameter
        Weight matrix.
    b : Parameter
        Bias vector.

    """

    def __init__(self, in_features, out_features, use_bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.use_bias = use_bias

        # register parameters 'w' and 'b' here (mind use_bias!)
        self.register_parameter('w', np.empty((out_features, in_features)))
        self.register_parameter('b', np.empty(
            out_features if use_bias else 0))  # __init__ so I put 100 here
        self.reset_parameters()

    def reset_parameters(self):
        """ Set initial values for parameters. """
        # input to hidden and hidden to output initialized with Xavier initialization
        gain = np.sqrt(2 / (self.in_features + self.out_features))
        self.w = np.random.randn(*self.w.shape) * gain
        if self.use_bias:
            self.b = np.zeros(*self.b.shape)

    def compute_outputs(self, x):
        """
        Parameters
        ----------
        x : (N, D) ndarray

        Returns
        -------
        s : (N, K) ndarrays
        cache : ndarray or iterable of ndarrays
        """

        s = x @ self.w.T

        if self.use_bias:
            s += self.b

        cache = x
        return s, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        dx : (N, D) ndarrays
        """
        x = cache

        if self.use_bias:
            self.b.grad = np.sum(grads, axis=0)

        self.w.grad = grads.T @ x

        return grads @ self.w


class LinearTransfrom(Module):
    """Simple module that preform linear transformation to matrix x given w and b"""

    def compute_outputs(self, x, w, b):
        """
        Parameters
        ----------
        x : ndarray
            Input matrix
        w : ndarray
            Weight matrix
        b : ndarray
            Bias vector

        Returns
        -------
        s : ndarray
            s = x @ w.T + b
        cache : tuple(ndarray)
            (x, w, b)
        """
        s = x @ w.T + b
        cache = (x, w, b)
        return s, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : ndarray
            Gradient ...
        cache : tuple(ndarray)
            (x, w, b)

        Returns
        -------
        d : tuple(ndarray)
            The gratient of dx, dw, dx
        """
        x, w, b = cache
        dx = (grads @ w).reshape(x.shape)
        dw = grads.T @ x
        db = np.sum(grads, axis=0)
        return dx, dw, db


class Dense(Linear):
    """Linear layer with activation"""

    def __init__(self, in_features, out_features, activation=None):
        """

        Parameters
        ----------
        in_features : int
            Number of input features
        out_features : int
            Number of output feature
        activation : Module
            Activation function (ReLU(), Sigmoid() ... )
        """
        self.activation = activation
        self.linear = LinearTransfrom()

        if self.activation is None:
            self.activation = Identity()

        super().__init__(in_features, out_features)

    def compute_outputs(self, x):
        """
        Parameters
        ----------
        x : (N, D) ndarray

        Returns
        -------
        s : (N, K) ndarrays
        cache : ndarray or iterable of ndarrays
        """

        a, fc_cache = self.linear.compute_outputs(x, self.w, self.b)

        out, activation_cache = self.activation.compute_outputs(a)

        cache = (fc_cache, activation_cache)

        return out, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : ndarray
            Gradient ...
        cache : tuple(ndarray)
            (x, w, b)

        Returns
        -------
        dx : ndarray
            The gratient of dx
        """

        fc_cache, activation_cache = cache

        da = self.activation.compute_grads(grads, activation_cache)

        dx, self.w.grad, self.b.grad = self.linear.compute_grads(da, fc_cache)

        return dx


class Sequential(Container):
    """
    Module that chains together multiple one-to-one sub-modules.
    """

    def __init__(self, *modules):
        super().__init__()
        if len(modules) == 1 and hasattr(modules[0], '__iter__'):
            modules = modules[0]

        for i, mod in enumerate(modules):
            self.add_module(mod)

    def compute_outputs(self, x):
        """
        Parameters
        ----------
        x : (N, D) ndarray

        Returns
        -------
        y : (N, K) ndarrays
        cache : ndarray or iterable of ndarrays
        """

        cache = []
        s = x

        for mod in self._modules:
            s, c = mod.compute_outputs(s)
            cache.append(c)

        return s, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        dx : (N, D) ndarrays
        """

        a = self._modules

        for mod, c in zip(reversed(a), reversed(cache)):
            grads = mod.compute_grads(grads, c)

        return grads

class Flatten(Module):
    """ Module to convert multi-dimensional outputs to a single vector. """

    def compute_outputs(self, x):
        return x.reshape(len(x), -1), x.shape

    def compute_grads(self, grads, shape):
        return grads.reshape(shape)


class Conv2D(Module):
    """ Numpy DL implementation of a 2D convolutional layer. """

    def __init__(self, in_channels, out_channels, kernel_size, use_bias=True):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.use_bias = use_bias

        # register parameters 'w' and 'b' here (mind use_bias!)
        # raise NotImplementedError("TODO: register parameters in Conv2D.__init__!")
        self.register_parameter('w', np.empty((out_channels, in_channels, kernel_size[0], kernel_size[1])))
        self.register_parameter('b', np.empty(out_channels if use_bias else 0))

        self.reset_parameters()

    def reset_parameters(self):
        """ Reset the parameters to some random values. """
        self.w = np.random.randn(*self.w.shape)
        if self.use_bias:
            self.b = np.random.randn(*self.b.shape)

    def compute_outputs(self, x):
        """
        Parameters
        ----------
        x : (N, Ci, H, W) ndarray

        Returns
        -------
        feature_maps : (N, Co, H', W') ndarray
        cache : ndarray or tuple of ndarrays
        """

        N, C, H, W = x.shape
        num_filters, _, filter_height, filter_width = self.w.shape

        pad, stride = 1, 1

        # Create output
        out_height = (H + 2 * pad - filter_height) // stride + 1
        out_width = (W + 2 * pad - filter_width) // stride + 1
        out = np.zeros((N, num_filters, out_height, out_width), dtype=x.dtype)

        x_cols = im2col_indices(x, self.w.shape[2], self.w.shape[3])
        res = self.w.reshape((self.w.shape[0], -1)).dot(x_cols) + self.b.reshape(-1, 1)

        out = res.reshape(self.w.shape[0], out.shape[2], out.shape[3], x.shape[0])
        out = out.transpose(3, 0, 1, 2)

        cache = (x, x_cols)
        return out, cache

    def compute_grads(self, grads, cache):
        """s
        Parameters
        ----------
        grads : (N, Co, H', W') ndarray
        cache : ndarray or tuple of ndarrays

        Returns
        -------
        dx : (N, Ci, H, W) ndarray
        """

        x, x_cols = cache

        db = np.sum(grads, axis=(0, 2, 3))

        pad, stride = 1, 1

        num_filters, _, filter_height, filter_width = self.w.shape
        dout_reshaped = grads.transpose(1, 2, 3, 0).reshape(num_filters, -1)
        dw = dout_reshaped.dot(x_cols.T).reshape(self.w.shape)

        dx_cols = self.w.reshape(num_filters, -1).T.dot(dout_reshaped)
        dx = col2im_indices(dx_cols, x.shape, filter_height, filter_width)

        self.w.grad = dw
        self.b.grad = db

        return dx


class MaxPool2d(Module):
    """ Numpy DL implementation of a max pooling layer. """

    def __init__(self, kernel_size):
        super().__init__()
        self.kernel_size = tuple(kernel_size)

    def compute_outputs(self, x):
        """
        Parameters
        ----------
        x : (N, C, H, W) ndarray

        Returns
        -------
        a : (N, C, H', W') ndarray
        cache : ndarray or tuple of ndarrays
        """
        N, C, H, W = x.shape
        pool_height, pool_width = self.kernel_size
        stride = 1

        out_height = (H - pool_height) // stride + 1
        out_width = (W - pool_width) // stride + 1

        x_split = x.reshape(N * C, 1, H, W)
        x_cols = im2col_indices(x_split, pool_height, pool_width, padding=0, stride=stride)
        x_cols_argmax = np.argmax(x_cols, axis=0)
        x_cols_max = x_cols[x_cols_argmax, np.arange(x_cols.shape[1])]
        out = x_cols_max.reshape(out_height, out_width, N, C).transpose(2, 3, 0, 1)

        cache = (x, x_cols, x_cols_argmax)
        return out, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, C, H', W') ndarray
        cache : ndarray or tuple of ndarrays

        Returns
        -------
        dx : (N, C, H, W) ndarray
        """
        x, x_cols, x_cols_argmax = cache
        pool_height, pool_width = self.kernel_size
        stride = 1
        N, C, H, W = x.shape

        dout_reshaped = grads.transpose(2, 3, 0, 1).flatten()
        dx_cols = np.zeros_like(x_cols)
        dx_cols[x_cols_argmax, np.arange(dx_cols.shape[1])] = dout_reshaped
        dx = col2im_indices(dx_cols, (N * C, 1, H, W), pool_height, pool_width,
                            padding=0, stride=stride)
        dx = dx.reshape(x.shape)

        return dx


class Dropout(Module):
    """ Implementation of (inverted) dropout. """

    def __init__(self, rate: float = .5, seed: int = None):
        """
        Parameters
        ----------
        rate : float, optional
            The percentage of neurons to be dropped.
        seed : int, optional
            Seed for the pseudo random generator.
        """
        super().__init__()
        if rate < 0. or rate > 1.:
            raise ValueError("dropout rate should be between zero and one")

        self.rate = float(rate)
        self.rng = np.random.RandomState(seed)

    def compute_outputs(self, x):
        if self.predicting:
            return x*self.rate
        else:
            multiplier = self.rng.binomial(1, 1 - self.rate, size=x.shape)
            return np.multiply(x, multiplier), multiplier

    def compute_grads(self, grads, multiplier):
        return grads * multiplier


class BatchNormalisation(Module):
    """Implementation of batch normalisation. """

    def __init__(self, dims: tuple, eps: float = 1e-8):
        """
        Parameters
        ----------
        dims : tuple of ints
            The shape of the incoming signal (without batch dimension).
        eps : float, optional
            Small value for numerical stability.
        """
        super().__init__()
        self.dims = tuple(dims)
        self.eps = float(eps)

        self.gamma = self.register_parameter('gamma', np.ones(self.dims))
        self.beta = self.register_parameter('beta', np.zeros(self.dims))

        self.running_count = 0
        self.running_stats = np.zeros((2,) + self.dims)

    def compute_outputs(self, x):
        if self.predicting:
            return x
        else:
            x_hat = (x - x.mean()) / (x.std())
            y_hat = self.gamma * x_hat + self.beta
            return y_hat, (x_hat, x, x.mean(), x.std() ** 2)

    def compute_grads(self, grads, cache):
        x_hat, x, x_mean, x_var = cache
        self.beta.grad = np.sum([g_i for g_i in grads], axis=0).reshape(self.beta.shape)
        self.gamma.grad = np.sum([grads_i * x_hat_i for grads_i in grads for x_hat_i in x_hat], axis=0).reshape(
            self.gamma.shape)
        d_x_hat = np.array([g_i * self.gamma for g_i in grads]).reshape(x_hat.shape)

        d_var = np.sum(
            [d_x_hat_i * (x_i - x_mean) * (-0.5) * ((x_var + self.eps) ** (-1.5)) for d_x_hat_i in d_x_hat for x_i in
             x])
        d_mean = np.sum([d_x_hat_i * (-1) / (np.sqrt(x_var + self.eps)) for d_x_hat_i in d_x_hat], axis=0) + d_var * (
            np.sum([(-2) * (x_i - x_mean) for x_i in x])) / len(x)
        dx = d_x_hat / (np.sqrt(x_var + self.eps)) + d_var * (2 * (x - x_mean)) / len(x) + d_mean / len(x)

        return dx
