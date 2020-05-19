# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-02-02 12:48:57'

import numpy
import pandas
import talib

# from .consts import *

"""
    部分指标计算：
        https://github.com/momintariq570/stocks-analysis-python/blob/79c332cd5666c15bac250af55453d6230b4d8cd5/technicals.py
"""


# noinspection PyUnresolvedReferences
def ema(closes: numpy.ndarray, period: int) -> numpy.ndarray:
    return talib.EMA(closes, timeperiod=period)


# noinspection PyUnresolvedReferences
def sma(closes: numpy.ndarray, period: int) -> numpy.ndarray:
    """
    SMA(MA) 简单移动平均值
    :param closes: 收盘价列表(日期升序排列)
    :param period: 周期(例如13日均线就传13)
    :return: SMA 列表
    """
    return talib.SMA(closes, timeperiod=period)


# noinspection PyUnresolvedReferences
def macd(closes: numpy.ndarray, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) \
        -> (numpy.ndarray, numpy.ndarray, numpy.ndarray):
    """
    MACD 异同移动平均线
    :param closes: 收盘价列表(日期升序排列)
    :param fast_period: 快速周期(一般为12)
    :param slow_period: 慢速周期(一般为26)
    :param signal_period: 反转信号周期(一般为9)
    :return: (差离值(DIF)列表，平滑移动平均线(DEA)列表，MACD列表)
    """
    # https://www.ricequant.com/community/topic/174//10
    # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
    # SMA：简单算术平均算法
    # EMA：指数平滑平均算法
    # WMA：加权移动平均算法
    # ...
    difs, deas, macds = talib.MACDEXT(closes,
                                      fastperiod=fast_period, fastmatype=1,
                                      slowperiod=slow_period, slowmatype=1,
                                      signalperiod=signal_period, signalmatype=1)
    macds = macds * 2
    return difs, deas, macds


def kdj(df: pandas.DataFrame):
    """
    https://www.cnblogs.com/eczhou/p/10647292.html
    :param df: K线数据，要求有low, high, close列
    """
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['k'] = pandas.DataFrame(rsv).ewm(com=2).mean()
    df['d'] = df['k'].ewm(com=2).mean()
    df['j'] = 3 * df['k'] - 2 * df['d']


# noinspection PyUnresolvedReferences
def sar(highs: numpy.ndarray, lows: numpy.ndarray) -> numpy.ndarray:
    # TODO 未搞定
    # return talib.SAR(highs, lows, acceleration=0.0224, maximum=20)
    # return talib.SAREXT(highs, lows, startvalue=0, offsetonreverse=0, accelerationinitlong=0.02, accelerationlong=0.02,
    #                     accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2)
    return talib.SAR(highs, lows)


def roc(closes: numpy.ndarray, period: int = 12, ma_period: int = 6) -> (numpy.ndarray, numpy.ndarray):
    """
    http://www.360doc.com/content/18/0522/11/33540468_756053176.shtml
    ROC指标有两种计算方法。
        第一种计算方法:
            ROC=[C(I)-C(I-N)]÷C(I-N)×100%
            C(I)为当日收盘价；C(I-N)为N日前的收盘价；N为计算参数。
        第二种计算方法:
            ROC (N日)=AX÷BX
            AX为今日的收盘价-N日前的收盘价；BX为N日前的收盘价；N为计算参数。
        其中，日ROC指标原始参数为10日。
        虽然以上两种计算方式不同，但其计算的结果是相同的。

        1. 当ROC向上表示强势，以0为中心线，由中心线下上穿大于0时，为买入信号
        2. 当ROC向下表示弱势，以0为中心线，由中心线上下穿小于0时，为卖出信号
        3. 当股价创新高时，ROC未能创新高，出现背离，表示头部形成
        4. 当股价创新低时，ROC未能创新低，出现背离，表示底部形成
        5. ROC与指标均线低位金叉，买入信号
        6. ROC与指标均线高位死叉，卖出信号

    :param closes:
    :param period:
    :param ma_period:
    :return:
    """
    df = pandas.DataFrame({'close': closes})
    df['ROC'] = (df['close'] - df['close'].shift(period)) / df['close'].shift(period) * 100
    df['MAROC'] = sma(df['ROC'], ma_period)
    return df['ROC'].values, df['MAROC'].values
