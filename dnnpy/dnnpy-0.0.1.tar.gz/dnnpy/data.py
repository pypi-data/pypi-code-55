import gzip
import os
import io
import tempfile
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from .utils import to_one_hot
import numpy as np

DEFAULT_PATH = os.path.join(os.path.expanduser("~"), ".znets")


class CachedDownload:
    """
    State of a possibly already cached download
    from a file at some URL to the local filesystem.
    """

    def __init__(self, base_url, file_name, base_path=None,
                 overwrite=False, block_size=4096):
        """
        Set up the cached download.

        Parameters
        ----------
        base_url : str
            URL that points to the directory where the file is located.
        file_name : str
            Name of the file that is to be downloaded.
        base_path : str, optional
            Path to the location where the downloaded file should be stored.
            If not specified, the file is stored in a temporary directory.
        overwrite : bool, optional
            Whether or not an existing local file should be overwritten.
        block_size : int, optional
            Number of bytes to read at once.
        """
        if base_path is None:
            base_path = tempfile.gettempdir()
        elif not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)

        self.url = '/'.join([base_url.rstrip('/'), file_name])
        self.file = os.path.join(base_path, file_name)
        self.block_size = block_size
        self.overwrite = overwrite

        try:
            self._response = urlopen(self.url)
            self._response.close()
        except HTTPError:
            raise ValueError("wrong URL? {}".format(self.url))
        except URLError:
            raise RuntimeError("could not connect to URL: {}".format(self.url))

    @property
    def file_name(self):
        """ Name of the file that is downloaded. """
        return os.path.basename(self.file)

    def _download_file(self):
        """ Download to file. """
        with open(self.file, 'wb') as fp:
            chunk = self._response.read(self.block_size)
            while chunk:
                fp.write(chunk)
                yield chunk
                chunk = self._response.read(self.block_size)

    def _read_file(self):
        """ Read from existing file. """
        with open(self.file, 'rb') as fp:
            chunk = fp.read(self.block_size)
            while chunk:
                yield chunk
                chunk = fp.read(self.block_size)

    def __enter__(self):
        self._response = urlopen(self.url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._response.close()

    def __iter__(self):
        if self.overwrite or not os.path.exists(self.file):
            return self._download_file()
        else:
            return self._read_file()

    def __len__(self):
        content_length = int(self._response.getheader('Content-Length', 0))
        return 1 + (content_length - 1) // self.block_size


MNIST_URL = "http://yann.lecun.com/exdb/mnist/"
MNIST_RAW = ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
             "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]


def get_mnist_data(path=None, test=False):
    """
    Load the MNIST dataset.

    Parameters
    ----------
    path : str, optional
        Path to directory where the dataset will be stored.
    test : bool, optional
        Flag to return test set instead of training data.

    Returns
    -------
    x : ndarray
        The input features in the data.
    y : ndarray
        The output labels in the data.
    """
    if path is None:
        path = os.path.join(DEFAULT_PATH, "mnist")

    arrays = []
    for file in MNIST_RAW:
        with CachedDownload(MNIST_URL, file, path) as chunks:
            data = gzip.decompress(b''.join(chunks))
            arr = _parse_idx(data)
            arrays.append(arr)

    if test is False:
        return tuple(arrays[:2])
    elif test is True:
        return tuple(arrays[2:])
    else:
        xs = np.concatenate(arrays[0::2], axis=0)
        ys = np.concatenate(arrays[1::2], axis=0)
        return xs, ys


def _parse_idx(data):
    """ Parse IDX file for vectors and multidimensional arrays. """
    import struct
    stream = io.BytesIO(data)
    zero, type_code, ndim = struct.unpack('HBB', stream.read(4))

    if zero != 0:
        raise ValueError("invalid data format")

    dtype_map = {
        0x08: 'uint8', 0x09: 'int8',
        0x0B: 'int16', 0x0C: 'int32',
        0x0D: 'float32', 0x0E: 'float64'
    }

    if type_code not in dtype_map:
        stream.close()
        raise ValueError("invalid type code: 0x{:02X}".format(type_code))

    dtype = np.dtype(dtype_map[type_code]).newbyteorder('>')
    shape = struct.unpack('>' + ndim * 'I', stream.read(4 * ndim))
    content = np.frombuffer(stream.read(), dtype)
    return content.reshape(shape)


def iris_data(path=None):
    """
    Get the data from the Iris dataset as numpy arrays.

    Parameters
    ----------
    path : str, optional
        Path to directory where the dataset will be stored.

    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, K) ndarray
        Vector of target labels.
    """
    base_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/"
    if path is None:
        path = os.path.join(os.getcwd(), "iris")

    with CachedDownload(base_url, "iris.data", path) as chunks:
        # store download as sequence of bytes
        raw_data = b''.join(chunks)

    data = [x.split(b',') for x in raw_data.split(b'\n') if x]  # Split data

    x, y = [], []

    for line in data:
        x.append(line[:-1])
        y.append(line[-1])  # y is in the last column

    unique = np.unique(y)
    y = to_one_hot([i for i in range(len(unique)) for a in y if a == unique[i]])
    # label + one hot encoder

    return np.array(x, float), np.array(y)


def split_data(x, y, ratio=.8):
    """
    Split a dataset in two parts with a given ratio.

    Parameters
    ----------
    x : ndarray
        Input features.
    y : ndarray
        Target values.
    ratio : float
        The percentage of samples in the first split.

    Returns
    -------
    (x1, y1) : tuple of ndarrays
        The first split of the dataset
    (x2, y2) : tuple of ndarrays
        The second split of the dataset

    Notes
    -----
    The order of the samples must not be maintained.
    """

    total = np.concatenate((x, y), axis=1)  # concatenate the data

    num_train = int(len(total) * ratio)  # number of training sample

    np.random.shuffle(total)  # shuffle the data

    x1 = total[:num_train, :x.shape[1]]  # x train
    y1 = total[:num_train, x.shape[1]:]  # y train

    x2 = total[num_train:, :x.shape[1]]  # x test
    y2 = total[num_train:, x.shape[1]:]  # y test

    return (x1, y1), (x2, y2)


def get_iris_data(path=None, test=False):
    """
    Get the correct split from the Iris dataset as numpy arrays.

    Parameters
    ----------
    path : str, optional
        Path to directory where the dataset will be stored.
    test : bool, optional
        Flag to return test set instead of training data.

    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, ) ndarray
        Vector of target labels.
    """
    x, y = iris_data(path)
    _train, _test = split_data(x, y, ratio=.8)
    return _test if test else _train


def abalone_data(path=None):
    """
    Get the data from the Abalone dataset as numpy arrays.

    Parameters
    ----------
    path : str, optional
        Path to directory where the dataset will be stored.

    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, ) ndarray
        Vector of target labels.
    """
    base_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/"
    if path is None:
        path = os.path.join(os.getcwd(), "abalone")

    with CachedDownload(base_url, "abalone.data", path) as chunks:
        # store download as sequence of bytes
        raw_data = b''.join(chunks)
    data = [x for x in raw_data.split(b'\n') if x]

    data = [x.split(b',') for x in raw_data.split(b'\n') if x]

    x, y, gender = [], [], []

    for line in data:
        x.append(line[1:-1])
        y.append(line[-1])
        gender.append(line[0])

    unique = np.unique(gender)

    gender = to_one_hot([i for i in range(len(unique)) for a in gender if a == unique[i]])

    x = np.array(np.concatenate((gender, x), axis=1), float)

    y = np.array(y)

    y = to_one_hot(y)
    return x, np.array(y.reshape(x.shape[0], -1), int)


def get_abalone_data(path=None, test=False):
    """
    Get the correct split from the Abalone dataset as numpy arrays.

    Parameters
    ----------
    path : str, optional
        Path to directory where the dataset will be stored.
    test : bool, optional
        Flag to return test set instead of training data.

    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, ) ndarray
        Vector of target labels.
    """
    x, y = abalone_data(path)
    _train, _test = split_data(x, y, ratio=.8)
    return _test if test else _train


# credit: http://cs231n.github.io/neural-networks-case-study/
def make_spiral_data(n_samples_per_class: int = 100, n_classes: int = 3, one_hot: bool = True, shuffle: bool = True) :
    """
    Parameters
    ----------
    n_samples_per_class : int
        Number of sample per class
    n_classes : int
        Number of class
    one_hot : Bool
        if True, apply one-hot to y
    shuffle : Bool
        if True, shuffle the data
    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, ) ndarray
        Vector of target labels.
    """
    dim = 2
    x = np.zeros((n_samples_per_class * n_classes, dim))
    y = np.zeros(n_samples_per_class * n_classes, dtype='uint8')
    for j in range(n_classes):
        ix = range(n_samples_per_class * j, n_samples_per_class * (j + 1))
        r = np.linspace(0.0, 1, n_samples_per_class)
        t = np.linspace(j * 4, (j + 1) * 4, n_samples_per_class) + np.random.randn(n_samples_per_class) * 0.2  # theta
        x[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[ix] = j
    if one_hot:
        y = to_one_hot(y)
    if shuffle:
        idx = np.random.permutation(len(x))
        x, y = x[idx], y[idx]
    return x, y


def make_XOR_data(n_samples: int = 100, one_hot: bool = False, dist: str = 'Uniform') :
    """
    Parameters
    ----------
    n_samples : int
        Number of sample to generate
    one_hot : Boolean
        if True, apply one-hot to y
    dist : str
        'Uniform' (Default), or 'Gaussian'

    Returns
    -------
    x : (N, D) ndarray
        Matrix of input features.
    y : (N, ) ndarray
        Vector of target labels.
    """
    if dist == 'Uniform':
        x = np.random.uniform(low=-1, high=1, size=(n_samples, 2))
    if dist == 'Gaussian':
        x = np.random.randn(n_samples)
    y = np.logical_xor(x[:, 0] > 0, x[:, 1] > 0).astype(np.int)
    if one_hot:
        y = to_one_hot(y)
    return x, y


def make_regression_data(n_samples: int = 100, n_features: int = 1, n_labels: int = 1):
    """
    Generate data for regression task
    Parameters
    ----------
    n_samples : int
        Number of samples to generate
    n_features : int
        Number of feature
    n_labels : int
        number of labels

    Returns
    -------
    (x, y) : tuple(ndarray)
    """
    x = np.random.randn(n_samples, n_features)
    w = np.random.randn(n_labels, n_features)
    b = np.random.randn(n_labels)

    noise = np.random.normal(0, np.random.uniform(0, 2), size=(n_samples, n_labels))
    y = (x @ w.T + b) + noise

    return x, y