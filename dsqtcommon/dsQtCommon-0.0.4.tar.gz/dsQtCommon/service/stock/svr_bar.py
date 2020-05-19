# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-31 19:45:13'

import datetime
from playhouse.shortcuts import model_to_dict
from dsPyLib.pandas.pandas_config import *
from dsPyLib.peewee.db_mgr import DBMgr
from dsQtCommon.models.stock.bar_base import DoesNotExist as BarDoesNotExist
from dsQtCommon.models.stock.bar_day import DBBarDay
from dsQtCommon.types.stock.types import *
from dsQtCommon.types.common.types import *


@DBMgr.close_database
def upsert_many_bars(bars: pandas.DataFrame, bar_model_cls):
    """
    批量插入股票K线数据(如果数据库中存在，则更新market, quality, name和fullname字段)
    :param bars: 股票K线数据
    :param bar_model_cls: 股票K线模型类
    """
    df = bars.copy()
    if len(df) == 0:
        return

    df['kind'] = df.apply(lambda x: x['kind'].value, axis=1)
    df['real_kind'] = df.apply(lambda x: x['real_kind'].value, axis=1)
    df['fq'] = df.apply(lambda x: x['fq'].value, axis=1)
    d = df.to_dict(orient='records')
    bar_model_cls.insert_many(d).on_conflict(
        conflict_target=[bar_model_cls.code, bar_model_cls.slot, bar_model_cls.fq],
        preserve=[bar_model_cls.open, bar_model_cls.high, bar_model_cls.low, bar_model_cls.close, bar_model_cls.volume,
                  bar_model_cls.amount,
                  bar_model_cls.change, bar_model_cls.amplitude, bar_model_cls.kind, bar_model_cls.real_kind,
                  bar_model_cls.turn],
    ).execute()


@DBMgr.close_database
def get_latest_slot(code: str, fq: StockBarFQ, bar_model_cls) -> datetime.datetime:
    """
    获取数据库中股票K线最新一条的时间槽，如果没有数据，则返回配置中指定的时间
    :param code: 股票代码
    :param fq: 复权方式
    :param bar_model_cls: 股票K线模型类
    :return: 时间槽
    """
    try:
        rec = bar_model_cls.select().where(
            (bar_model_cls.code == code) & (bar_model_cls.fq == fq.value)
        ).order_by(bar_model_cls.slot.desc()).limit(1).get()
        return rec.slot
    except BarDoesNotExist:
        daily_bar_first_date = '2006-01-01'  # 日、周、月K线数据，时间范围：2006-01-01至今
        minute_bar_first_date = '2011-01-01'  # 5、15、30、60分钟K线数据，时间范围：2011-01-01至今

        if bar_model_cls is DBBarDay:
            date_str = daily_bar_first_date
        else:
            date_str = minute_bar_first_date
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")


@DBMgr.close_database
def query_bars(code: str, fq: StockBarFQ, bar_model_cls, limit: int = 0) -> pandas.DataFrame or None:
    """
    从数据库中查询股票的K线数据(结果按照时间槽升序排列)
    :param code: 股票代码
    :param fq: 复权方式
    :param bar_model_cls: 股票K线模型类
    :param limit: 取多少条数据
    :return: DataFrame
    """
    try:

        dataset = bar_model_cls.select().where(
            (bar_model_cls.code == code) & (bar_model_cls.fq == fq.value)
        ).order_by(bar_model_cls.slot.desc()).limit(limit)
        df = _dataset_to_df(dataset)
        df = df.iloc[::-1]  # 反序，这样就按照日期升序排列了
        return df
    except BarDoesNotExist:
        return None


def _dataset_to_df(dataset) -> pandas.DataFrame:
    """
    将模型查询出来的数据集转换为DataFrame
    :param dataset: 数据集
    :return: DataFrame
    """
    datas = list()
    for rec in dataset:
        d = model_to_dict(rec)
        d['kind'] = BarKind(d['kind'])
        d['real_kind'] = BarKind(d['real_kind'])
        d['fq'] = StockBarFQ(d['fq'])
        datas.append(d)

    df = pandas.DataFrame(datas)
    return df
