from . import Module
import numpy as np


class Identity(Module):
    """ Implementation of the identity function. """

    def compute_outputs(self, s):
        return s, None

    def compute_grads(self, grads, cache):
        return grads


class Tanh(Module):
    """Implementation of the hyperbolic tangent function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = np.tanh(s)
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = (1 - (np.tanh(s)) ** 2) * grads

        return ds


class Sigmoid(Module):
    """Implementation of the identity function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = 1 / (1 + np.exp(-s))

        cache = a
        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        a = cache

        ds = a * (1 - a) * grads

        return ds


class ReLU(Module):
    """Implementation of the Rectified Linear Unit. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = s * (s > 0)
        cache = s
        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache
        ds = grads * (1 * (s > 0))
        return ds


class ELU(Module):
    """Implementation of the Exponential Linear Unit. """

    def __init__(self, alpha=1.):
        super().__init__()
        if alpha < 0:
            raise ValueError("negative values for alpha are not allowed")

        self.alpha = alpha

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = s * (s > 0) + self.alpha * (np.exp(s) - 1) * (s < 0)
        cache = s
        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache
        ds = grads * (1 * (s > 0)) + grads * (self.alpha * (np.exp(s)) * (s < 0))
        return ds


class SeLU(Module):
    """Implementation of the Scaled Exponential Linear Unit. """

    def __init__(self):
        super().__init__()

        self.alpha = 1.6732632423543772848170429916717
        self.lamb = 1.0507009873554804934193349852946

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = self.lamb * s * (s > 0) + self.lamb * (self.alpha * (np.exp(s) - 1)) * (s <= 0)
        cache = s
        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache
        ds = grads * (self.lamb * (s > 0)) + grads * (self.lamb * self.alpha * (np.exp(s)) * (s <= 0))
        return ds


class ISRU(Module):
    """Implementation of the ISRU function. """

    def __init__(self, alpha=1):

        super().__init__()

        self.alpha = alpha

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = s / np.sqrt(1 + self.alpha * s * s)
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = (1 / np.sqrt(1 + self.alpha * s * s)) ** 3

        return ds


class SoftPlus(Module):
    """Implementation of the SoftPlus function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = np.log(1 + np.exp(s))
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = 1 / (1 + np.exp(-s))

        return ds


class BentIdentity(Module):
    """Implementation of the BentIdentity function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = (np.sqrt(s * s + 1) - 1) / 2 + s
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = s / (2 * np.sqrt(s * s + 1)) + 1

        return ds


class Gaussian(Module):
    """Implementation of the Gaussian function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = np.exp(-s * s)
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = -2 * s * np.exp(-s * s)

        return ds


class Softsign(Module):
    """Implementation of the Softsign function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = s / (1 + np.abs(s))
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = 1 / (1 + np.abs(s)) ** 2

        return ds


class HardTanh(Module):
    """Implementation of the hard hyperbolic tangent function. """

    def compute_outputs(self, s):
        """
        Parameters
        ----------
        s : (N, K) ndarray

        Returns
        -------
        a : (N, K) ndarray
        cache : ndarray or iterable of ndarrays
        """
        a = -1 * (s < -1) + s * (-1 <= s <= 1) + 1 * (s > 1)
        cache = s

        return a, cache

    def compute_grads(self, grads, cache):
        """
        Parameters
        ----------
        grads : (N, K) ndarray
        cache : ndarray or iterable of ndarrays

        Returns
        -------
        ds : (N, K) ndarrays
        """
        s = cache

        ds = (1 * (-1 <= s <= 1)) * grads

        return ds
