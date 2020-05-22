import numpy as np
import math
from scipy.special import comb


def pwm(x, n=4):
    r"""Return a list with the n first probability weighted moments (:math:`b_r`).

    .. math::
           b_r = \frac{\sum_{i=1}^{n_s} x_i  {i \choose r}}{n_s {n_s - 1\choose r}}

    where:

        :math:`n_s` --- size of the sample *x*

    See, for example, `Diana Bilkova (2014) <http://file.scirp.org/Html/1-1720182_49981.htm>`_ (eq. 17)

    :param x: sample values
    :type x: list or numpy.array
    :param n: number of returned probability weighted moments (:math:`b_r`)
    :type n: 
    :return: (*list*) probability weighted moments (:math:`b_r`)
    """
    x = np.sort(x)
    ns = len(x)
    return [sum([comb(i, r) * x[i] for i in range(ns)]) / (ns * comb(ns - 1, r)) for r in range(n)]


def lmoments(x, n=4, ratio=True, lcv=False):
    r"""Return a list with the n first L-moments of the sample x.

    .. math::
           \lambda_{r + 1} = \sum_{k=0}^{r} (-1)^{r - k} {r \choose k} {r + k \choose k} b_k

    with:

        :math:`0 \leq r \leq n - 1`

    where:

        :math:`b_k` --- first probability weighted moments (see :func:`pwm`)


    See, for example, `Diana Bilkova (2014) <http://file.scirp.org/Html/1-1720182_49981.htm>`_ (eq. 26)

    If ratio is True, replace :math:`\lambda_r` with :math:`\lambda_r/\lambda_2` for :math:`r \geq 3`, where
    :math:`\lambda_3/\lambda_2` is the L-skewness and :math:`\lambda_4/\lambda_2` is the L-kurtosis.

    If lcv is True, replace :math:`\lambda_2` with the coefficient of L-variation :math:`\lambda_2/\lambda_1`.
    For a non-negative random variable, this lies in the interval (0,1) and is identical to the Gini coefficient
    (see https://en.wikipedia.org/wiki/L-moment).

    :param x: sample values
    :type x: list or numpy.array
    :param n: number of returned probability weighted moments (:math:`b_r`)
    :type n: int
    :param ratio: if True, replace :math:`\lambda_r` with :math:`\lambda_r/\lambda_2` for :math:`r \geq 3`.
      Default :math:`ratio = True`
    :type ratio: bool
    :param lcv: if True, replace :math:`\lambda_2` with :math:`\lambda_2/\lambda_1`
    :type lcv: bool
    :return: (*list*) L-moments of the sample x
    """
    b = pwm(x, n)
    result = [sum([(-1)**(r-k) * comb(r, k) * comb(r + k, k) * b[k] for k in range(r+1)]) for r in range(n)]
    if ratio:
        result[2:] = [r / result[1] for r in result[2:]]
    if lcv:
        result[1] /= result[0]
    return result


def lmoments_parameter_estimation_generalized_logistic(lambda1, lambda2, tau):
    """Return the location, scale and shape or the generalized logistic distribution

    Based on SUBROUTINE PELGLO of the LMOMENTS Fortran package version 3.04, July 2005

    :param lambda1: L-moment-1
    :param lambda2: L-moment-2
    :param tau:  L-moment-3 /  L-moment-2
    :return: (*float*) location, scale and shape
    """
    assert lambda2 > 0 and -1 < -tau < 1
    try:
        k = -tau
        a = math.sin(k * math.pi) / (k * math.pi)
        s = lambda2 * a
        m = lambda1 - (s / k) * (1.0 - 1.0 / a)
        return m, s, k
    except ZeroDivisionError:
        return lambda1, lambda2, 0.0


def lmoments_parameter_estimation_gamma(lambda1, lambda2):
    """Return the location and scale of the gamma distribution.

    Based on SUBROUTINE PELGAM of the LMOMENTS Fortran package version 3.04, July 2005

    :param lambda1: L-moment-1 (:math:`\lambda_1`)
    :type lambda1: float
    :param lambda2: L-moment-2 (:math:`\lambda_2`)
    :type lambda12: float
    :return: (*float*) location and scale
    """
    if lambda1 <= lambda2 or lambda2 <= 0.0:
        return None, None
    cv = lambda2 / lambda1
    if cv >= 0.5:
        t = 1.0 - cv
        alpha = t * (0.7213 - t * 0.5947) / (1.0 + t * (-2.1817 + t * 1.2113))
    else:
        t = math.pi * cv * cv
        alpha = (1.0 - 0.3080 * t) / (t * (1.0 + t * (-0.05812 + t * 0.01765)))
    return alpha, lambda1/alpha


def genloglogistic_cdf(x, loc, scale, shape):
    """Return the cumulative distribution function of the generalized logistic distribution

    Based on SUBROUTINE CDFGLO of the LMOMENTS Fortran package version 3.04, July 2005


    :param x: sample values
    :type x: numpy.array
    :param loc: location parameter (:math:`\mu`)
    :type loc: float
    :param scale: scale parameter (:math:`\sigma` > 0)
    :type scale: float
    :param shape: shape parameter (:math:`\kappa`)
    :type shape: float
    :return: (*numpy.array*) cdf
    """
    x = (x - loc) / scale
    try:
        a = 1.0 - shape * x
        if a > 1e-15 or shape == 0.0:
            x = np.log(a) / shape
            return 1.0 / (1 + np.exp(x))
        return 0.0 if shape < 0.0 else 1.0
    except ZeroDivisionError:
        return 1.0 / (1 + np.exp(-x))
