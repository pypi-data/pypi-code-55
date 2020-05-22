import numpy as np
from scipy.stats import norm, gamma
from caeli.distributions import genloglogistic_cdf, lmoments, lmoments_parameter_estimation_gamma, \
    lmoments_parameter_estimation_generalized_logistic
from caeli.time_series import months_split_annually


# =============================================================================
# SPI
# =============================================================================
def spi(precipitation):
    """
    :param precipitation: meteo values
    :type precipitation: list or np.array
    :return: list of spi
    :rtype: list
    """
    try:
        precipitation = np.array(precipitation)
    except AttributeError:
        pass
    if precipitation is None:
        return np.array([])
    isna = np.isnan(precipitation)
    i_vl = np.argwhere(~isna).ravel()
    i_gz = np.argwhere(~(isna | (precipitation == 0))).ravel()
    result = np.full(len(precipitation), np.nan)
    if len(i_vl) < 2:
        return result
    lambda1, lambda2 = lmoments(precipitation[i_gz], 2)
    alpha, beta = lmoments_parameter_estimation_gamma(lambda1, lambda2)
    f = len(i_gz) / len(i_vl)
    for i, p in enumerate(precipitation):
        if not np.isnan(p):
            result[i] = norm.ppf((1 - f) + f * gamma.cdf(p, alpha, scale=beta))
    return result


def spi_monthly(sr, months=range(1, 13), aggregation=1, start_at=None,
                closed_left=True, closed_right=False, label='left',
                is_sorted=False, prefix='P', min_years=20):
    """

    :param sr: Series with precipitation depth
    :type sr:
    :param months: list of months, e.g. [11, 12, 1, 2, 3]
    :type months:
    :param aggregation: number of months to aggregate: 1, 2, 3, 4, or 6. Default: n=1
    :type aggregation:
    :param start_at:
    :param closed_left:
    :param closed_right:
    :param label:
    :param is_sorted:
    :param prefix:
    :param min_years:
    :return: pandas.DataFrame with precipitations 'Prec' and drought indices 'Spi' for each year and month
    """
    df = months_split_annually(sr, rule='sum', months=months, aggregation=aggregation, start_at=start_at,
                               closed_left=closed_left, closed_right=closed_right, label=label,
                               is_sorted=is_sorted, prefix=prefix)
    if len(df.index) < min_years:
        return None
    for c in df.columns:
        df['SPI{}'.format(c[len(prefix):])] = spi(df[c].values)
    return df


# =============================================================================
# SPEI
# =============================================================================
def spei(values):
    """Calculate SPEI from given values.

    Values are the differences between meteo and potential evapotranspiration.

    For example if you want to calculate spei from January in the


    :param values: list or numpy array of values
    :type values: list, numpy array
    :return:
    :rtype:
    """
    try:
        values = np.array(values)
    except AttributeError:
        pass
    if values is None:
        return np.array([])
    result = np.full(len(values), np.nan)
    i_vl = np.argwhere(~np.isnan(values)).ravel()
    if len(i_vl) < 2:
        return result

    lambda1, lambda2, tau3 = lmoments(values[i_vl], 3)
    location, scale, shape = lmoments_parameter_estimation_generalized_logistic(lambda1, lambda2, tau3)
    for i, pr_et in enumerate(values):
        if not np.isnan(pr_et):
            cdf = genloglogistic_cdf(pr_et, location, scale, shape)
            result[i] = norm.ppf(cdf)
    return result


def spei_monthly(sr, months=range(1, 13), aggregation=1, start_at=None,
                 closed_left=True, closed_right=False, label='left',
                 is_sorted=False, prefix='P', min_years=20):
    """

    :param sr: Series with precipitation depth minus potential evapotranspiration (:math:`P - ETo`) as values and
      pandas TimeStamp as index. The series frequencies can be, for example, minutely, hourly, daily, or monthly.
    :type sr: pandas series
    :param months: list of months, e.g. [11, 12, 1, 2, 3]
    :type months: list
    :param aggregation: number of months to aggregate: 1, 2, 3, 4, or 6. Default: n=1
    :type aggregation:
    :param start_at:
    :type :
    :param closed_left:
    :type :
    :param closed_right:
    :type :
    :param label:
    :type :
    :param is_sorted:
    :type :
    :param prefix:
    :type :
    :param min_years:
    :type :
    :return: (**)
    """
    """
    :param prefix:
    :type prefix:
    :param min_years:
    :type min_years:
    :return: pandas.DataFrame with precipitations 'Prec' and drought indices 'Spi' for each year and month
    :rtype:
    """
    df = months_split_annually(sr, rule='sum', months=months, aggregation=aggregation, start_at=start_at,
                               closed_left=closed_left, closed_right=closed_right, label=label,
                               is_sorted=is_sorted, prefix=prefix)
    if len(df.index) < min_years:
        return None
    for c in df.columns:
        df['SPEI{}'.format(c[len(prefix):])] = spei(df[c].values)
    return df
