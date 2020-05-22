import os
import unittest
import numpy as np
import pandas as pd
from caeli.drought_indices import spi, spi_monthly, spei, spei_monthly
from caeli.time_series import monthly_intervals, monthly_series, months_split_annually


def spi_01():
    p = [286.08, 321.11, 260.34, 383.07, 277.56, 150.5, 272.63, 246.31, 254.92, 288.5,
         267.12, 242.51, 286.56, 285.43, 370.03, 241.54, 233.65, 336.29, 330.73, 360.46,
         407.13, 381.74, 217.2, 232.68, 418.64, 338.96, 246.49, 391.28, 223.81, 387.61]
    print(spi(p))


def spi_02():
    p = [np.nan, 321.11, 260.34, 383.07, 277.56, 150.5, 272.63, 246.31, 254.92, 288.5,
         267.12, 242.51, 286.56, 285.43, 370.03, 241.54, 233.65, 336.29, 330.73, 360.46,
         407.13, 381.74, 217.2, 232.68, 418.64, 338.96, 246.49, 391.28, np.nan, 387.61]
    print(spi(p).round(1))


def spi_03():
    np.random.seed(1)
    index = pd.date_range('1990-01-01', '2019-12-31', freq='1d')
    values = np.random.normal(1, 0.7, len(index))
    values[values < 0] = 0.0
    df = pd.DataFrame({'P': values}, index=index)
    df_spi = spi_monthly(df, aggregation=3).round(1)
    with pd.option_context('display.max_rows', 4, 'display.max_columns', 8, 'display.width', 1000):
        print(df_spi)


def spei_01():
    p = [236.78906908, 264.81174819, 206.07614488, 329.1471248, 229.76300328, 88.48107583, 222.12576411, 203.1740944,
         194.24915861, 233.04840882, 203.03193236, 181.99807424, 228.55427209, 239.45338575, 316.16425044, 192.11761111,
         173.18384051, 285.25591321, 275.19281235, 310.7161464, 348.84101779, 330.42774158, 163.55803563, 177.16544205,
         359.67310805, 282.82742497, 191.03543726, 333.89194558, 163.25115185, 322.16858475]
    print(spei(p))


def spei_02():
    p = [np.nan, 264.81174819, 206.07614488, 329.1471248, 229.76300328, 88.48107583, 222.12576411, 203.1740944,
         194.24915861, 233.04840882, 203.03193236, 181.99807424, 228.55427209, 239.45338575, 316.16425044, 192.11761111,
         173.18384051, 285.25591321, 275.19281235, 310.7161464, 348.84101779, 330.42774158, 163.55803563, 177.16544205,
         359.67310805, 282.82742497, 191.03543726, 333.89194558, np.nan, 322.16858475]
    print(spei(p).round(2))


def spei_03():
    np.random.seed(1)
    index = pd.date_range('1990-01-01', '2019-12-31', freq='1d')
    values = np.random.normal(1, 0.7, len(index))
    values[values < 0] = 0.0
    df = pd.DataFrame({'P-PET': values}, index=index)
    df_spei = spei_monthly(df, aggregation=3).round(1)
    with pd.option_context('display.max_rows', 4, 'display.max_columns', 8, 'display.width', 1000):
        print(df_spei)


def ts_ex01():
    index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')  # pd.DatetimeIndex(date_range)
    print('{}, {}, ..., {}, {}'.format(index[0], index[1], index[-2], index[-1]))

    itv = monthly_intervals(index, months=None, aggregation=1, start_at='beg', closed_left=True, closed_right=True)
    print('{}, ..., {}'.format(itv[0], itv[-1]))

    itv = monthly_intervals(index, months=None, aggregation=1, start_at='1999-01-01 07:30', closed_left=True, closed_right=True)
    print('{}, ..., {}'.format(itv[0], itv[-1]))

    itv = monthly_intervals(index, months=None, aggregation=1, start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
    print('{}, ..., {}'.format(itv[0], itv[-1]))

    itv = monthly_intervals(index, months=None, aggregation=2, start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
    print('{}, ..., {}'.format(itv[0], itv[-1]))

    itv = monthly_intervals(index, months=[1, 4, 7, 10], aggregation=3, start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
    print('{}, ..., {}'.format(itv[0], itv[-1]))

    itv = monthly_intervals(index, months=[2, 5, 8, 11], aggregation=-3, start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
    print('{}, ..., {}'.format(itv[0], itv[-1]))


def ts_ex02():
    with pd.option_context('display.max_rows', 4, 'display.max_columns', 30, 'display.width', 1000):
        np.random.seed(1)
        index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')  # pd.DatetimeIndex(date_range)
        p = np.random.normal(2, 0.1, size=len(index))
        p[p < 0.0] = 0.0
        sr_daily = pd.Series(p, index=index)

        sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30')
        print(sr_monthly)

        sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30', time_format=None)
        print(sr_monthly)

        sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30', label='left')
        print(sr_monthly)

        sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30', label='left', time_format=None)
        print(sr_monthly)


def ts_ex03():
    with pd.option_context('display.max_rows', 4, 'display.max_columns', 4, 'display.width', 1000):
        np.random.seed(1)
        index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')  # pd.DatetimeIndex(date_range)
        p = np.random.normal(2, 0.1, size=len(index))
        p[p < 0.0] = 0.0
        sr_daily = pd.Series(p, index=index)

        spy = months_split_annually(sr_daily, aggregation=2, start_at='1999-01-01 07:30')
        print(spy)

        spy = months_split_annually(sr_daily, aggregation=2, start_at='1999-01-01 07:30', time_format=None)
        print(spy)

        spy = months_split_annually(sr_daily, aggregation=2, start_at='1999-01-01 07:30', label='left')
        print(spy)

        spy = months_split_annually(sr_daily, aggregation=2, start_at='1999-01-01 07:30', label='left', time_format=None)
        print(spy)


if __name__ == '__main__':
    pass
    # spi_01()
    # spi_02()
    spi_03()
    # spei_01()
    # spei_02()
    # spei_03()
    # ts_ex01()
    # ts_ex02()
    # ts_ex03()

