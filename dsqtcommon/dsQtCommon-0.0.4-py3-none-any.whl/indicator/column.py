# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-31 18:54:21'

import math
from dsQtCommon.types.common.types import *
from dsQtCommon.indicator.indicator import *

"""
    指标
"""


# 添加K线类型列
def add_col_kind(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    在K线数据的DataFrame中新增一列'kind'，代表K线的类型

    :param df: 数据(要求包含close列)
    :return: 添加了real_kind列的K线数据
    """
    col = 'kind'
    df[col] = BarKind.cross
    df.loc[df[df['close'] > df['open']].index, col] = BarKind.positive
    df.loc[df[df['close'] < df['open']].index, col] = BarKind.negative
    return df


# 添加K线真实类型列
def add_col_real_kind(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    在K线数据的DataFrame中新增一列'real_kind'，代表K线的真实类型，其中：
        如果是假阳真阴，则看做阴线
        如果是假阴真阳，则看做阳线
        其余与'kind'列相同

    假阴真阳(跳空高开低走，收盘价高于上一根的收盘价，并收出阴线)
        逻辑：当前是阴线 and (收盘价 > 前一根收盘价)
    假阳真阴(跳空低开高走，收盘价低于上一根的收盘价，并收出阳线)
        逻辑：当前是阳线 and (收盘价 < 前一根收盘价)

    :param df: 数据(要求包含close列)
    :return: 添加了real_kind列的K线数据
    """
    col = 'real_kind'
    df[col] = df['kind']
    df.loc[df[(df['kind'] == BarKind.negative) & (df['close'] > df['close'].shift())].index, col] = BarKind.positive
    df.loc[df[(df['kind'] == BarKind.positive) & (df['close'] < df['close'].shift())].index, col] = BarKind.negative
    return df


def add_col_ema(df: pandas.DataFrame, period: int, precision: int = 3) -> pandas.DataFrame:
    """
    添加EMA
    :param df: 数据(要求包含close列)
    :param period: 周期数
    :param precision: 小数保留位数
    :return: 包含了所添加移动平均值的K线数据(列名为 ema周期数，例如13日均线的列名为：ema13)
    """
    key = f'ema{period}'
    ma = ema(df['close'].values, period)
    df[key] = ma
    df = df.round({key: precision})
    return df


def add_col_ma(df: pandas.DataFrame, period: int, precision: int = 3) -> pandas.DataFrame:
    """
    添加移动平均指标值
    :param df: 数据(要求包含close列)
    :param period: 周期数
    :param precision: 小数保留位数
    :return: 包含了所添加移动平均值的K线数据(列名为 ma周期数，例如13日均线的列名为：ma13)
    """
    key = f'ma{period}'
    ma = sma(df['close'].values, period)
    df[key] = ma
    df = df.round({key: precision})
    return df


def add_col_macd(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    添加MACD数据
    :param df: 数据(要求包含close列)
    :return: 包含了MACD数据的K线数据(新增列名：dif, dea, macd)
    """
    difs, deas, macds = macd(df['close'].values)
    df['dif'] = difs
    df['dea'] = deas
    df['macd'] = macds
    df = df.round({'dif': 5, 'dea': 5, 'macd': 5})
    return df


def add_col_kdj(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    添加KDJ数据
    :param df: 数据(要求包含low, high, close列)
    :return: 包含了KDJ数据的K线数据(新增列名：k, d, j)
    """
    kdj(df)
    df = df.round({'k': 2, 'd': 2, 'j': 2})
    return df


def add_col_sar(df: pandas.DataFrame, digit: int = 3) -> pandas.DataFrame:
    """
    添加SAR数据
    :param df: 数据(要求包含low, high列)
    :param digit: 精度
    :return: 包含了SAR数据(新增列名：sar)
    """
    df['sar'] = sar(df['high'].values, df['low'].values)
    df = df.round({'sar': digit})
    return df


def add_col_roc(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    添加ROC数据
    :param df: 数据(要求包含close列)
    :return: 新增列：roc, maroc
    """
    rocs, ma_rocs = roc(df['close'])
    df['roc'] = rocs
    df['maroc'] = ma_rocs
    df = df.round({'roc': 2, 'maroc': 2})
    return df


def add_col_sar_reverse(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    添加SAR反转数据
    :param df: 数据(要求包含low, high列)
    :return: 新增列：sar_reverse, 由下转上(多转空) ==> -1；未转换 ==> 0；由上转下(空转多) ==> 1
    """
    df['sar_reverse'] = 0
    df.loc[df[(df['sar'].shift() < df['low'].shift()) & (df['SAR'] > df['high'])].index, 'sar_reverse'] = -1
    df.loc[df[(df['sar'].shift() > df['high'].shift()) & (df['SAR'] < df['low'])].index, 'sar_reverse'] = 1
    return df


def add_col_ma_cross(df: pandas.DataFrame, ma: str) -> pandas.DataFrame:
    """
    添加均线穿越K线的状态：下穿 ==> -1; 未穿 ==> 0; 上穿 ==> 1
    例如，想添加MA13的穿越K线状态：
        add_ma_cross(df, 'ma13')，返回列名：'ma13_cross'
    :param df: 数据(要求包含kind, close，均线 列)
    :param ma: 均线的名称

    算法：
        上一根K线的收盘价在均线的一边，这一根K线的收盘价在均线的另一边
        或者
        K线的开盘价和收盘价分别在均线的两边
    """

    # 上一根K线的收盘价在均线的一边，这一根K线的收盘价在均线的另一边(跳空)
    ma = ma.lower()
    key = f'{ma}_cross'
    df[key] = 0
    df.loc[df[(df['kind'] == -1) & (df[ma].shift() < df['close'].shift()) & (df[ma] > df['close'])].index, key] = -1
    df.loc[df[(df['kind'] == 1) & (df[ma].shift() > df['close'].shift()) & (df[ma] < df['close'])].index, key] = 1

    # K线的开盘价和收盘价分别在均线的两边
    def cross(p_open: float, p_close: float, p_ma: float, org) -> int:
        if (p_open <= p_ma) and (p_close >= p_ma):
            return 1
        if (p_open >= p_ma) and (p_close <= p_ma):
            return -1
        return org

    df[key] = df.apply(lambda x: cross(x['open'], x['close'], x[ma], x[key]), axis=1)

    return df


def add_col_forward(df: pandas.DataFrame, ind: str) -> pandas.DataFrame:
    """
    添加指标的方向(与上一根K线相比)，-1 ==> 向下；0 ==> 平；1 ==> 向上
    例如，想添加ma13的方向：
        add_forward(df, 'ma13')，会生成 ma13_forward 列

    :param df: 数据
    :param ind: 指标的列名(大小写敏感)
    """
    key = ind.lower() + '_forward'
    df[key] = 0
    df.loc[df[df[ind] < df[ind].shift()].index, key] = -1
    df.loc[df[df[ind] > df[ind].shift()].index, key] = 1
    return df


def add_col_position(df: pandas.DataFrame, ind: str, ref: str) -> pandas.DataFrame:
    """
    添加指标的位置，生成的指标列名为：{ind}_{ref}_position
    如果：
        ind < ref，也就是说 ind 在 ref 的下方，值为-1
        ind = ref，也就是说 ind 与 ref 位置相同，值为0
        ind > ref，也就是说 ind 在 ref 的上方，值为1
    例如：
        add_position(df, 'ma13', 'ma34')，用于判断ma13相对于ma34的位置，生成的列名为：ma13_ma34_position

    :param df: 数据
    :param ind: 是要计算位置的指标
    :param ref: 是用于参照的指标
    """

    def position(p_ind: float, p_ref: float) -> int:
        if p_ind < p_ref:
            return -1
        if p_ind > p_ref:
            return 1
        return 0

    col = f'{ind}_{ref}_position'
    df[col] = df.apply(lambda x: position(x[ind], x[ref]), axis=1)
    return df


def add_col_golden(df: pandas.DataFrame, ind: str, ref: str) -> pandas.DataFrame:
    """
    添加指标的金叉状态，生成的指标列名为：{ind}_{ref}_golden
    如果：
        当前根K线，ind 与 ref 形成死叉，值为-3
        上一根K线，ind 与 ref 形成死叉，值为-2
        上上根K线，ind 与 ref 形成死叉，值为-1
        其它，值为0
        上上根K线，ind 与 ref 形成金叉，值为1
        上一根K线，ind 与 ref 形成金叉，值为2
        当前根K线，ind 与 ref 形成金叉，值为3
    例如：
        add_golden(df, 'k', 'd')，生成的列名为：d_d_golden

    :param df: 数据
    :param ind: 要判断金叉状态的指标
    :param ref: 用于参照的指标
    """
    col = f'{ind}_{ref}_golden'
    df[col] = 0
    df.loc[df[(df[ind].shift(2) < df[ref].shift(2)) & (df[ind].shift(3) > df[ref].shift(3))].index, col] = -1
    df.loc[df[(df[ind].shift(2) > df[ref].shift(2)) & (df[ind].shift(3) < df[ref].shift(3))].index, col] = 1
    df.loc[df[(df[ind].shift(1) < df[ref].shift(1)) & (df[ind].shift(2) > df[ref].shift(2))].index, col] = -2
    df.loc[df[(df[ind].shift(1) > df[ref].shift(1)) & (df[ind].shift(2) < df[ref].shift(2))].index, col] = 2
    df.loc[df[(df[ind].shift(0) < df[ref].shift(0)) & (df[ind].shift(1) > df[ref].shift(1))].index, col] = -3
    df.loc[df[(df[ind].shift(0) > df[ref].shift(0)) & (df[ind].shift(1) < df[ref].shift(1))].index, col] = 3
    return df


def add_col_ma_flat(df: pandas.DataFrame, ind: str) -> pandas.DataFrame:
    """
    判断均线是否走平
        如果 abs(均线值(上个) - 均线值(当前)) / 均线值(当前) < 0.0006，则认为走平了
    :param df: 数据
    :param ind: 均线的列名，如果走平，值为1，否则为0
    :return:
    """
    col = f'{ind}_flat'
    df[col] = 0
    df.loc[df[(abs(df[ind].shift(1) - df[ind]) / df[ind]) < 0.0006].index, col] = 1
    return df


def add_entity_max(df: pandas.DataFrame, period: int) -> pandas.DataFrame:
    """
    添加一定周期内柱体大值最大值列
    会新增4列：
        entity_max                      柱体最大值
        entity_max_{period}             指定周期的内柱体最大值
        is_prev_entity_max_{period}     前一根K线是否为指定周期内柱体最大值
        is_entity_max_{period}          当前K线是否为指定周期内柱体最大值
    :param df: 数据(要求包含open, close列)
    :param period: 周期
    :return:
    """
    df['entity_max'] = df.apply(lambda x: max(x['open'], x['close']), axis=1)
    df[f'entity_max_{period}'] = df['entity_max'].shift().rolling(period, min_periods=period).max()
    df[f'is_prev_entity_max_{period}'] = (df['entity_max'].shift() == df[f'entity_max_{period}'])
    df[f'is_entity_max_{period}'] = (df['entity_max'] >= df[f'entity_max_{period}'])
    return df


def add_entity_min(df: pandas.DataFrame, period: int) -> pandas.DataFrame:
    """
    添加一定周期内柱体小值最小值列
    会新增4列：
        entity_min                      柱体最小值
        entity_min_{period}             指定周期的内柱体最小值
        is_prev_entity_min_{period}     前一根K线是否为指定周期内柱体最小值(True/False)
        is_entity_min_{period}          当前K线是否为指定周期内柱体最小值(True/False)
    :param df: 数据(要求包含open, close列)
    :param period: 周期
    :return:
    """
    df['entity_min'] = df.apply(lambda x: min(x['open'], x['close']), axis=1)
    df[f'entity_min_{period}'] = df['entity_min'].shift().rolling(period, min_periods=period).min()
    df[f'is_prev_entity_min_{period}'] = (df['entity_min'].shift() == df[f'entity_min_{period}'])
    df[f'is_entity_min_{period}'] = (df['entity_min'] >= df[f'entity_min_{period}'])
    return df


def add_triangle(df: pandas.DataFrame, ind: str, horizontal_unit: int = 3) -> pandas.DataFrame:
    """
    计算指定key前后两个值形成的弧度和角度
        在列表中添加两个字段
        radian_{ind}: 弧度
        angle_{ind}: 角度
    :param df: K线列表
    :param ind: 列名
    :param horizontal_unit: 两条K线之间的水平距离
    :return:
    """
    df[f'delta_{ind}'] = df[ind] - df[ind].shift()
    df[f'radian_{ind}'] = df.apply(lambda x: math.atan(x[f'delta_{ind}'] / horizontal_unit), axis=1)
    df[f'angle_{ind}'] = 180 / math.pi * df[f'radian_{ind}']
    return df


# noinspection NonAsciiCharacters,PyPep8Naming
def add_col_yang_bao_yin(df: pandas.DataFrame) -> pandas.DataFrame or None:
    """
    在DataFrame中添加阳包阴标志列(yang_yao_yin)
    逻辑：
        1. 用最后三根K线进行判断，最后一根命名为k1，倒数第二根为k2，倒数第三根为k3
        2. k1是阳线，k2是阴线 (K线开盘价和收盘价判断)
        3. k1的收盘价大于等于K2的开盘价
        4. 如果K2和K3之间存在跳空缺口，则K1的收盘价需要大于等于k3的柱体低值

    :param df: K线数据
    :return: True/False
    """

    if df is None:
        return None

    # k2开盘价
    df['k2_open'] = df['open'].shift()

    # k3柱体低值
    df['k3_min'] = df[['open', 'close']].shift(2).min(axis=1)

    # 跳空价(如果没跳空，则为k2的开盘价)
    df['gap'] = df[['k2_open', 'k3_min']].max(axis=1)

    # 阳包阴标志
    df['yang_bao_yin'] = False
    df.loc[df[
               (df['open'] < df['close'])  # k1是阳线
               & (df['open'].shift() > df['close'].shift())  # k2是阴线
               & (df['close'] >= df['gap'])  # k1的收盘价吃掉了k2的开盘价(包括跳空)
               & (df['volume'] > df['volume'].shift())  # 量也吃掉
               ].index, 'yang_bao_yin'] = True

    # 删除临时的列
    df.drop(['k2_open', 'k3_min', 'gap'], axis=1, inplace=True)

    return df
