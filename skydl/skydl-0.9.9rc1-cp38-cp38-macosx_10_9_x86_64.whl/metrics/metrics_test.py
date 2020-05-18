from pandas import date_range, DataFrame
from skydl.metrics import build_merged_factory_price_data, factory_mean_ic, factory_ir


def _average_cumulative_return_by_quantile(before=1, after=2, demeaned=False, quantiles=4):
    expected_vals = [[1.00, 0.0, -0.50, -0.75],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.00, 0.00, 0.00, 0.00],
                     [0.0, 0.0, 0.0, 0.0],
                     [-0.20, 0.0, 0.25, 0.5625],
                     [0.0, 0.0, 0.0, 0.0],
                     [-0.3333333, 0.0, 0.50, 1.25],
                     [0.0, 0.0, 0.0, 0.0]]
    from pandas import (
        DataFrame,
        date_range,
        MultiIndex
    )
    from skydl.alphalens import tears, performance, plotting, utils
    from pandas.util.testing import assert_frame_equal
    dr = date_range(start='2015-1-15', end='2015-2-1')
    dr.name = 'date'
    tickers = ['A', 'B', 'C', 'D']
    r1, r2, r3, r4 = (1.25, 1.50, 1.00, 0.50)
    data = [[r1 ** i, r2 ** i, r3 ** i, r4 ** i] for i in range(1, 19)]
    prices = DataFrame(index=dr, columns=tickers, data=data)
    dr2 = date_range(start='2015-1-21', end='2015-1-26')
    dr2.name = 'date'
    factor = DataFrame(
        index=dr2, columns=tickers, data=[
            [3, 4, 2, 1],
            [3, 4, 2, 1],
            [3, 4, 2, 1],
            [3, 4, 2, 1],
            [3, 4, 2, 1],
            [3, 4, 2, 1]])

    factor_data = build_merged_factory_price_data(
        factor, prices, quantiles=quantiles, periods=range(
            0, after + 1), filter_zscore=False)

    avgrt = performance.average_cumulative_return_by_quantile(
        factor_data, prices, before, after, demeaned)
    arrays = []
    for q in range(1, quantiles + 1):
        arrays.append((q, 'mean'))
        arrays.append((q, 'std'))
    index = MultiIndex.from_tuples(arrays, names=['factor_quantile', None])
    expected = DataFrame(
        index=index, columns=range(-before, after + 1), data=expected_vals)
    assert_frame_equal(avgrt, expected)


def _get_clean_factor_and_forward_returns_1():
    """
    Test get_clean_factor_and_forward_returns with a daily factor
    """
    import numpy as np
    tickers = ['A', 'B', 'C', 'D', 'E', 'F']
    factor_groups = {'A': "板块1", 'B': "板块2", 'C': "板块1", 'D': "板块2", 'E': "板块1", 'F': "板块2"}
    price_data = [[1.20**i, 0.50**i, 3.00**i, 0.90**i, 0.50**i, 1.00**i]
                  for i in range(1, 10)]  # 6 days = 3 + 3 fwd returns
    factor_data = [[33, 43, 23, 11, 13, 22],
                   [32, 34, 78, 21, 14, 2],
                   [31, 22, 24, 31, 24, 22]]  # 3 days
    start = '2015-1-11'
    factor_end = '2015-1-13'
    price_end = '2015-1-19'  # 日期往后移动3天，3D fwd returns

    price_index = date_range(start=start, end=price_end)
    price_index.name = 'date'
    prices = DataFrame(index=price_index, columns=tickers, data=price_data)

    factor_index = date_range(start=start, end=factor_end)
    factor_index.name = 'date'
    factor = DataFrame(index=factor_index, columns=tickers,
                       data=factor_data)

    merged_data = build_merged_factory_price_data(
        factor, prices,
        groupby=factor_groups,
        quantiles=4,
        periods=(1, 2, 3))
    mean_ic = factory_mean_ic(merged_data, by_group=True)
    print(mean_ic)


if __name__ == '__main__':
    _get_clean_factor_and_forward_returns_1()
