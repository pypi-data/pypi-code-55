# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-30 22:37:04'

from playhouse.shortcuts import model_to_dict
from dsPyLib.pandas.pandas_config import *
from dsPyLib.peewee.db_mgr import DBMgr
from dsQtCommon.models.stock.meta import DBStockMeta, DoesNotExist as DBMetaDoesNotExist
from dsQtCommon.types.stock.types import *


@DBMgr.close_database
def upsert_many_stocks(stocks: pandas.DataFrame):
    """
    批量插入股票元信息(如果数据库中存在，则更新market, quality, name和fullname字段)
    :param stocks: 股票元信息
    """
    df = stocks.copy()
    if len(df) == 0:
        return

    df['exchange'] = df.apply(lambda x: x['exchange'].value, axis=1)
    df['market'] = df.apply(lambda x: x['market'].value, axis=1)
    df['quality'] = df.apply(lambda x: x['quality'].value, axis=1)
    d = df.to_dict(orient='records')
    DBStockMeta.insert_many(d).on_conflict(
        conflict_target=[DBStockMeta.code],
        preserve=[DBStockMeta.market, DBStockMeta.quality, DBStockMeta.name, DBStockMeta.full_name],  # 冲突时保留的字段(会被更新的值)
    ).execute()


# 查询所有股票
@DBMgr.close_database
def query_all_stocks() -> pandas.DataFrame or None:
    try:
        dataset = DBStockMeta.select()
        df = _dataset_to_df(dataset)
        return df
    except DBMetaDoesNotExist:
        return None


# 查询所有股票(不包括指数、ST和*ST)
def query_stocks_without_index_st() -> pandas.DataFrame or None:
    df = query_all_stocks()
    if df is None:
        return None
    else:
        df = df.loc[
            # 过滤掉ST和*ST
            (df['quality'] == StockQuality.normal)
            # 过滤掉指数
            & ((df['market'] != StockMarket.sh_index) & (df['market'] != StockMarket.sz_index))
            ]
        return df


def _dataset_to_df(dataset) -> pandas.DataFrame:
    """
    将模型查询出来的数据集转换为DataFrame
    :param dataset: 数据集
    :return: DataFrame
    """
    datas = list()
    for rec in dataset:
        d = model_to_dict(rec)
        d['exchange'] = StockExchange(d['exchange'])
        d['market'] = StockMarket(d['market'])
        d['quality'] = StockQuality(d['quality'])
        datas.append(d)

    df = pandas.DataFrame(datas)
    return df
