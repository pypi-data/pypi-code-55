import numpy as np


def to_one_hot(y, k: int = None):
    """
    Compute a one-hot encoding from a vector of integer labels.

    Parameters
    ----------
    y : (N, ) ndarray
        The zero-indexed integer labels to encode.
    k : int, optional
        The number of distinct labels in `y`.

    Returns
    -------
    one_hot : (N, k) ndarray
        The one-hot encoding of the labels.
    """
    y = np.asarray(y, dtype='int')
    n = len(y)
    if k is None:
        k = np.amax(y) + 1

    one_hot = np.zeros((n, k))
    one_hot[np.arange(n), y] = 1
    return one_hot


def split_data(x, y, ratio=0.7):
    """
    Split up a dataset in two subsets with a specific ratio.

    Parameters
    ----------
    x : ndarray
        Input features.
    y : ndarray
        Target values.
    ratio : int or float, optional
        If an integer is provided,
        the first split will have `ratio` as many sample as the second split.
        A value between 0.5 and 1 corresponds to
        the percentage of data that goes to the first split.

    Returns
    -------
    (x1, y1) : tuple of ndarrays
        The first, larger split of the dataset.
    (x2, y2) : tuple of ndarrays
        The second, smaller split of the dataset.
    """
    # not the most efficient solution, but elegant
    step = int(1 / (1 - ratio)) if ratio < 1 else int(ratio) + 1
    idx = slice(None, None, step)
    x1, x2 = np.delete(x, idx, axis=0), x[idx]
    y1, y2 = np.delete(y, idx, axis=0), y[idx]
    return (x1, y1), (x2, y2)


def sig2col(x, w_shape, stride=1, dilation=1):
    """
    Represent signal so that each 'column' represents
    the elements in a sliding window.

    Parameters
    ----------
    x : ndarray
        The signal to represent.
    w_shape : tuple of ints
        The shape of the window.
        The length defines the dimensionality.
    stride : int or tuple of ints, optional
        The stride(s) for each dimension of the window.
    dilation : int or tuple of ints, optional
        The dilation(s) for each dimension of the window.

    Returns
    -------
    cols : ndarray
        New representation of the array.
        This array will have `len(w_shape)` more dimensions than `x`.

    Notes
    -----
    This function implements the 'im2col' trick,
    used for implementing convolutions efficiently.
    """
    w_shape = np.asarray(w_shape)
    x_shape1, x_shape2 = np.split(x.shape, [-len(w_shape)])
    kernel_shape = dilation * (w_shape - 1) + 1
    out_shape2 = (x_shape2 - kernel_shape) // stride + 1

    # sliding window view (inspired by http://github.com/numpy/numpy/pull/10771)
    x_si1, x_si2 = np.split(x.strides, [len(x_shape1)])
    v_strides = tuple(x_si1) + tuple(stride * x_si2) + tuple(dilation * x_si2)
    v_shape = tuple(x_shape1) + tuple(out_shape2) + tuple(w_shape)
    _x = np.lib.stride_tricks.as_strided(x, v_shape, v_strides, writeable=False)
    return _x


class Dataloader:

    def __init__(self, x, y, batch_size=None, shuffle=False):
        self.x = x
        self.y = y
        self.batch_size = len(x) if batch_size is None else int(batch_size)
        self.shuffle = shuffle

    def __iter__(self):
        """
        Iterates over the samples of the data.

        Yields
        ------
        x : ndarray
            input features for the batch
        y : ndarray
            target values for the batch

        Notes
        -----
        Each batch should contain the specified number of samples,
        except for the last batch if the batch_size does
        not divide the number of samples in the data.
        """
        x, y = np.copy(self.x), np.copy(self.y)

        idx = np.random.permutation(len(x))

        x, y = x[idx], y[idx]

        n = self.batch_size
        for i in range(0, len(x), n):
            yield x[i: i + n], y[i: i + n]

    def __len__(self):
        return 1 + (len(self.x) - 1) // self.batch_size


def to_label(y):
    return list(map(np.argmax, y))