from abc import abstractmethod

import tensorflow as tf
import numpy as np


__ALL__ = ["MultiVarDiagonalGaussian", "BaseDistribution"]

class BaseDistribution(object):
    """
    The :class:`BaseDistribution` class is the base class for various probabilistic distributions.
    It support sampling from the distribution, evaluating (log-)probabilities at given values,
    and computing the kl-divergence between this distribution and a given distribution.
    """
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def sample(self):
        pass

    @abstractmethod
    def log_prob(self, inputs):
        pass

    @abstractmethod
    def prob(self, inputs):
        pass

    @abstractmethod
    def kl_divergence(self, dist):
        pass


class MultiVarDiagonalGaussian(BaseDistribution):
    """
    The :class:`DiagonalGaussian` class is the multivariate Gaussian distribution with diagonal covariance.

    It supports batch inputs, generating batches of samples, evaluating (log-)probabilities at batches of
    given values, and computing the KL-divergence between itself and another given distribution.

    The typical shape for distribution parameters is ``batch_shape + value_shape``.
    The ``batch_shape`` represents how many independent inputs are fed into the distribution at the same time.
    The ``value_shape`` represents the shape of non-batch values of this distribution.
    Both ``mean`` and ``log_variance`` share the same shape.

    Samples generated are of shape ``([n_samples]+) batch_shape + value_shape``.
    The first additional axis omitted only when passed n_samples is None (by default), in which case one sample is
    generated.
    For a uni-variate distribution, its value_shape is ``TensorShape([])``.
    For a multi-variate distribution, its value_shape is ``TensorShape([N])``, where N is an integer.

    When evaluating (log-)probabilities at given values, the given values should be of the shape
    ``([n_samples]+) batch_shape + value_shape``.
    The returned Tensor has shape ``([n_samples]+) batch_shape``.

    When computing KL-divergence given another distribution,
    the given distribution should have the same ``batch_shape`` and ``value_shape``.
    The returned Tensor has shape ``batch_shape``.

    Both parameters and samples have the same type, which equals ``dtype``.
    When two or more have different type, TypeError will be raised.

    Parameters
    ----------
    mean:
        the mean value of the distribution.
    log_variance:
        The diagonal covariance value of the distribution.
    dtype:
        The type of samples/parameters of the distribution.
    """
    def __init__(self, mean, log_variance, dtype, name):
        BaseDistribution.__init__(self, name)

        self._log_variance = tf.convert_to_tensor(log_variance)
        self._mean = tf.convert_to_tensor(mean)
        self._dtype = dtype

        # check shape
        self._mean.get_shape().assert_is_compatible_with(self._log_variance.get_shape())
        self._batch_shape = self._mean.get_shape()[:-1]
        self._value_shape = self._mean.get_shape()[-1]


    @property
    def mean(self):
        """The mean value of the distribution. It has shape ``batch_shape + value_shape``."""
        return self._mean

    @property
    def log_variance(self):
        """The diagonal covariance value of the distribution. It has shape ``batch_shape + value_shape``."""
        return self._log_variance

    @property
    def dtype(self):
        """The type of samples/parameters of the distribution."""
        return self._dtype

    @property
    def batch_shape(self):
        """
        The shape showing how many independent inputs are fed into the distribution at the same time.

        Returns
        -------
        batch_shape: A TensorShape object.
        """
        return self._batch_shape

    @property
    def value_shape(self):
        """
        The shape showing the non-batch values of this distribution.

        Returns
        -------
        value_shape: A TensorShape object.
        """
        return self._value_shape

    def _sample(self):
        """
        Generate one sample from the distribution.

        Returns
        -------
            A sample of shape ``batch_shape + value_shape``.
        """
        epsilon = tf.random_normal(tf.shape(self._log_variance), name="epsilon")
        std = tf.exp(0.5 * self._log_variance)
        z = self._mean + tf.multiply(std, epsilon)
        return z

    def sample(self, n_samples=None):
        """
        Generate multiple samples from the distribution.

        Parameters
        ----------
        n_samples: an integer
            The number of samples.

        Returns
        -------
        Samples: a Tensor
            Multiple samples of shape ``[n_samples] + batch_shape + value_shape``.
        """
        if n_samples is None:
            return self._sample()
        ret = []
        for _ in range(n_samples):
            ret.append(tf.expand_dims(self._sample(), axis=0))
        return tf.concat(ret, 0)


    def log_prob(self, inputs):
        """
        Evaluating the log-probabilities of the distribution at given values.

        Parameters
        ----------
        inputs: a Tensor
            Given values of shape ``([n_samples] +) batch_shape + value_shape``.
        """
        return -0.5 * tf.reduce_sum(
            tf.log(2 * np.pi) + self._log_variance +
            tf.div(tf.pow((inputs - self._mean), 2), tf.exp(self._log_variance)),
                                    reduction_indices=-1)

    def prob(self, inputs):
        """
        Evaluating the probabilities of the distribution at given values.

        Parameters
        ----------
        inputs: a Tensor
            Given values of shape ``([n_samples] +) batch_shape + value_shape``.
        """
        raise NotImplementedError()


    def kl_divergence(self, dist):
        """
        Computing KL[current_distribution || dist].

        Parameters
        ----------
        dist: a BaseDistribution object
            Another given distribution.
        Returns
        -------
        KLD: a Tensor
            The KL divergence between current distribution and the given distribution.
        """
        given_dist = self._check_dist_shape(dist)

        prior_logvar = given_dist.log_variance
        prior_mu = given_dist.mean

        kld = -0.5 * tf.reduce_sum(1 + (self._log_variance - prior_logvar)
                               - tf.div(tf.pow(prior_mu - self._mean, 2), tf.exp(prior_logvar))
                               - tf.div(tf.exp(self._log_variance), tf.exp(prior_logvar)), reduction_indices=-1)
        return kld


    def _check_dist_shape(self, dist):
        """
        Check whether the given distribution shares the same shape as current distribution.

        Parameters
        ----------
        dist: a BaseDistribution object
            Another given distribution.
        """
        logvar = dist.log_variance
        mean = dist.mean
        err_msg = "The given distribution should match 'batch_shape + value_shape' of current distribution."
        try:
            logvar.get_shape().assert_is_compatible_with(mean.get_shape())
            logvar.get_shape().assert_is_compatible_with(self.log_variance.get_shape())
        except ValueError:
            raise ValueError(
                err_msg + "(given: {} and {} | current: {})".format(
                        logvar.get_shape(), mean.get_shape(), self.log_variance.get_shape())
            )
        return dist