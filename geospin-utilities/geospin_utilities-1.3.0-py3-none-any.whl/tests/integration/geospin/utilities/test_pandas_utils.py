import pandas as pd
import numpy as np
import pytest


def test_remove_outliers_percentile():
    from geospin.utilities.pandas_utils import remove_outliers_percentile
    # Are the lower and upper outliers of ten examples removed?
    df = pd.DataFrame(
        index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        data=dict(
            my_col=[45., 48, 87, 99.5, 34., 0.1, 32., 77., 81, 28]
        )
    )
    expected = pd.DataFrame(
        index=[1, 2, 3, 5, 7, 8, 9, 10],
        data=dict(
            my_col=[45., 48, 87, 34., 32., 77., 81, 28]
        )
    )
    actual = remove_outliers_percentile(df, column='my_col', lower=10, upper=90)
    pd.testing.assert_frame_equal(expected, actual)


def test_remove_outliers_iqr():
    from geospin.utilities.pandas_utils import remove_outliers_iqr
    # In a normal distribution, we expect to find a fraction of
    # (0.5 + 2 * 0.2465) non-fliers.
    # See: https://en.wikipedia.org/wiki/Interquartile_range

    # Create gaussian distribution
    np.random.seed(0)
    n = 1000000
    random_numbers = np.random.randn(n)
    df = pd.DataFrame(
        data=dict(
            my_col=random_numbers
        )
    )
    # Expected number of non-fliers
    n_non_fliers_expected = n * (0.5 + 2 * 0.2465)

    df_wo_outliers = remove_outliers_iqr(df, column='my_col')
    # Actual number of non-fliers
    n_non_fliers_actual = len(df_wo_outliers['my_col'])

    assert n_non_fliers_expected / n == pytest.approx(n_non_fliers_actual /
                                                      n, abs=0.001)
