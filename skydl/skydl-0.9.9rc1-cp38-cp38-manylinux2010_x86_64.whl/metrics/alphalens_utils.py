"""
ziplien alphalens(V0.4.0) wrapper
参考：因子看板 https://www.joinquant.com/view/factorlib/list
https://github.com/quantopian/alphalens
"""
import pandas as pd
from skydl.alphalens import performance, utils


def build_merged_factory_price_data(factor,
                                   prices,
                                   groupby=None,
                                   quantiles=5,
                                   periods=(1, 5, 10)):
    """
    get merged factory and price data
    link: tears.create_full_tear_sheet(merged_data)
    :param merged_data e.g. factor_data & prices
    :return:
    """
    return utils.get_clean_factor_and_forward_returns(factor.stack(),
                                                        prices,
                                                        groupby=groupby,
                                                        quantiles=quantiles,
                                                        periods=periods)


def std_information_coefficient(factor_data,
                                 group_adjust=False,
                                 by_group=False,
                                 by_time=None):
    """
    ic标准方差(Computes the Spearman Rank Correlation based Information Coefficient (IC))
    参考：alphalens#mean_information_coefficient：https://github.com/quantopian/alphalens/blob/0492c9d53670994c5ed14bf630bea25a5efc219a/alphalens/performance.py#L76
    Get the mean information coefficient of specified groups.
    Answers questions like:
    What is the mean IC for each month?
    What is the mean IC for each group for our whole timerange?
    What is the mean IC for for each group, each week?
    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    group_adjust : bool
        Demean forward returns by group before computing IC.
    by_group : bool
        If True, take the mean IC for each group.
    by_time : str (pd time_rule), optional
        Time window to use when taking mean IC.
        See http://pandas.pydata.org/pandas-docs/stable/timeseries.html
        for available options.

    Returns
    -------
    ic : pd.DataFrame
        Mean Spearman Rank correlation between factor and provided
        forward price movement windows.
    """
    rank_ic = performance.factor_information_coefficient(factor_data, group_adjust, by_group)
    grouper = []
    if by_time is not None:
        grouper.append(pd.Grouper(freq=by_time))
    if by_group:
        grouper.append('group')
    if len(grouper) == 0:
        ic = rank_ic.std()
    else:
        ic = (rank_ic.reset_index().set_index('date').groupby(grouper).mean())
    return ic


def factory_mean_ic(merged_data, by_group=False):
    """
    单因子IC均值(Computes the Spearman Rank Correlation based Information Coefficient (IC))
    IC:信息系数(Information Coefficient,简称 IC)，代表因子预测股票收益的能力。
    IC的计算方法是：计算全部股票在调仓周期期初排名和调仓周期期末收益排名的线性相关度(Correlation)。
    IC越大的因子，选股能力就越强。
    """
    return performance.mean_information_coefficient(merged_data, by_group=by_group)


def factory_ir(merged_data, by_group=False):
    """
    单因子IR值
    IR:信息比率(Information Ratio,简称IR)= IC的多周期均值/IC的标准方差，代表因子获取稳定Alpha的能力。
    整个回测时段由多个调仓周期组成，每一个周期都会计算出一个不同的IC值，IR等于多个调仓周期的IC均值除以这些IC的标准方差。
    所以IR兼顾了因子的选股能力（由IC代表）和因子选股能力的稳定性（由IC的标准方差的倒数代表）。
    另：ic_summary_table["Ann. IR"] = (ic_data.mean() / ic_data.std()) * np.sqrt(252) https://github.com/quantopian/alphalens/issues/208
    :return:
    """
    return factory_mean_ic(merged_data, by_group) / std_information_coefficient(factor_data=merged_data, by_group=by_group)


def rank_ic(factor_data,
             group_adjust=False,
             by_group=False,
             by_time=None):
    """
    rankIC可以用来构建IC时序图: x: rankIC, y: 22日移动平均
    IC是本期因子值和下期股票收益的秩相关系数，通常
    用以评价预测能力。取值在-1到1之间，绝对值越大，
    表示预测能力越好。(这里用rank IC计算)
    :return:
    """
    return performance.factor_information_coefficient(factor_data, group_adjust, by_group)