from nltk.translate.bleu_score import sentence_bleu
import numpy as np
from nltk.util import ngrams
import math
import tensorflow as tf


def gaussian_kld(posterior_mu, posterior_logvar, prior_mu, prior_logvar):
    """
    Calculate the KL divergence between posterior distribution and prior distribution.

    In mathematical statistics, the KL(Kullback–Leibler) divergence is a measure of how
    one probability distribution is different from a second, reference probability
    distribution.

    In particular, if two distributions are gaussian distribution, the KL divergence can
    be calculated as:

    :math:`KL(p, q) = log(\delta_1) - log(\delta_2) + (\delta_1^2+(\mu_1 - \mu_2)^2)/(2*\delta_2^2) -0.5`

    where :math:`p` is the posterior distribution with :math:`\delta_1` as its standard
    deviation and :math:`\mu_1` as its mean, :math:`q` is the prior distribution with
    :math:`\delta_2` as its standard deviation and :math:`\mu_2` as its mean.

    References:
        https://arxiv.org/pdf/1606.05908.pdf
        https://www.cnblogs.com/yutingmoran/p/8631186.html

    Parameters
    ----------
    posterior_mu : tf.tensor
        the mean of posterior distribution, the shape is (batch_size * posterior_dim)
    posterior_logvar : tf.tensor
        the log of the covariance of posterior distribution, the shape is (batch_size * posterior_dim)
    prior_mu : tf.tensor
        the mean of prior distribution, the shape is (batch_size * prior_dim)
    prior_logvar : tf.tensor
        the log of the covariance of prior distribution, the shape is (batch_size * prior_dim)

    Returns
    -------
    KL_divergence : tf.tensor
        the shape is (batch_size,)
    """
    kld = -0.5 * tf.reduce_sum(1 + (posterior_logvar - prior_logvar)
                               - tf.div(tf.pow(prior_mu - posterior_mu, 2), tf.exp(prior_logvar))
                               - tf.div(tf.exp(posterior_logvar), tf.exp(prior_logvar)), reduction_indices=1)
    return kld


def standard_gaussian_kld(posterior_mu, posterior_logvar):
    """
    Calculate the KL divergence between posterior distribution and standard gaussian distribution.

    This is the special case of gaussian_kld() function where the prior distribution
    is standard gaussian distribution. Now the expression is:

    :math:`KL(p, q) = log(\delta_1) + (\delta_1^2+\mu_1^2)/2 -0.5`

    where :math:`p` is the posterior distribution with :math:`\delta_1` as its standard
    deviation and :math:`\mu_1` as its mean, :math:`q` is the standard gaussian
    distribution with 0 as mean, and 1 as standard deviation.

    References:
        https://arxiv.org/pdf/1606.05908.pdf
        https://www.cnblogs.com/yutingmoran/p/8631186.html

    Parameters
    ----------
    posterior_mu : tf.tensor
        the mean of posterior distribution, the shape is (batch_size * posterior_dim)
    posterior_logvar : tf.tensor
        the log of the covariance of posterior distribution, the shape is (batch_size * posterior_dim)

    Returns
    -------
    KL_divergence : tf.tensor
        the shape is (batch_size,)
    """
    kld = - 0.5 * tf.reduce_sum(1 + posterior_logvar
                                - tf.exp(posterior_logvar)
                                - tf.pow(posterior_mu, 2), reduction_indices=1)
    return kld