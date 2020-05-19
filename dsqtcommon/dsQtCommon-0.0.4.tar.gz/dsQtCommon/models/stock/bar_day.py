# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-31 19:40:43'

from dsQtCommon.models.stock.bar_base import DBBaseBar


class DBBarDay(DBBaseBar):
    """ 股票日K数据 """

    class Meta:
        table_name = 'bar_day'
