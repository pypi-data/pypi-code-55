# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-23 21:14:34'

import datetime
import baostock
from dsPyLib.utils.timez import date_to_str, str_to_date
from dsPyLib.pandas.data_frame import is_col_exists
from dsQtCommon.types.stock.types import *
from dsQtCommon.indicator.column import *

"""
    API文档
    http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3
"""

daily_bar_first_date = '2006-01-01'  # 日、周、月K线数据，时间范围：2006-01-01至今
minute_bar_first_date = '2011-01-01'  # 5、15、30、60分钟K线数据，时间范围：2011-01-01至今


class BaoStock(object):

    def __init__(self):
        self.all_stocks = None  # 所有股票元数据

        baostock.login()
        self.fresh_stocks()

    def fresh_stocks(self):
        """
        刷新股票元数据(更新属性)
        :return:
        """
        self.all_stocks = self.query_all_stock()

    def is_trade_date(self, date: datetime.datetime = datetime.datetime.now()) -> bool:
        """
        判断指定日期是否为交易日
        :param date: 指定日期，默认为当前时间
        :return: True: 是交易日; False: 不是交易日
        """
        s_date = date_to_str(date)
        df = self.query_trade_dates(start_date=s_date, end_date=s_date)
        ret = (df.iloc[-1]['is_trading_day'] == '1')
        return ret

    # noinspection PyMethodMayBeStatic
    def get_latest_trade_date(self) -> str:
        """
        获取最近的交易日
        :return: str, 最近的交易日(%Y-%m-%d)
        """
        # 获取四周之内的交易日信息
        end_date = datetime.datetime.now()
        # 如果当前时间小于09:30，则结束时间取前一天
        if (end_date.hour < 9) or (end_date.hour == 9 and end_date.minute < 30):
            end_date = end_date + datetime.timedelta(days=-1)
        start_date = end_date + datetime.timedelta(weeks=-4)
        s_start = date_to_str(start_date)
        s_end = date_to_str(end_date)
        df = self.query_trade_dates(s_start, s_end)

        # 获取最新的交易日
        if len(df) > 0:
            ret = df.iloc[-1]['calendar_date']
            return ret
        else:
            raise Exception('未能正确的获取到最近的交易日！')

    # noinspection PyMethodMayBeStatic
    def get_prev_trade_date(self, date: datetime.date) -> datetime.date:
        """
        获取指定日期之前的最后一个交易日
        :param date: 日期
        :return: 之前最后一个交易日
        """
        # 获取指定日期四周之内的交易日信息
        start_date = date + datetime.timedelta(weeks=-4)
        s_start = date_to_str(start_date)
        s_end = date_to_str(date)
        df = self.query_trade_dates(s_start, s_end)

        # 获取指定日期之前的最后一个交易日
        df = df.loc[df['calendar_date'] < s_end]
        if len(df) > 0:
            ret = df.iloc[-1]['calendar_date']
            return ret
        else:
            raise Exception(f'未能正确的获取到{s_start}之前的最后一个交易日！')

    # noinspection PyMethodMayBeStatic
    def get_stock_code(self, exchange: StockExchange, number: str) -> str:
        """
        根据交易所和股票六位数字代码，生成BaoStock的股票编码
        :param exchange: 交易所
        :param number: 股票六位数字代码
        :return: BaoStock的股票编码
        """
        ret = f'{exchange.value}.{number}'
        return ret

    # noinspection PyMethodMayBeStatic
    def query_trade_dates(self, start_date: str = daily_bar_first_date,
                          end_date: str = None) -> pandas.DataFrame:
        """
        查询出给定范围的交易日(返回的列表中只有交易日，非交易日不会列出来)

        @param start_date: 起始日期，默认2015-01-01 (%Y-%m-%d)
        @param end_date: 终止日期，默认当前日期 (%Y-%m-%d)
        @return: calendar_date 日期；is_trading_day，是否交易日，0:非交易日;1:交易日
        """
        rs = baostock.query_trade_dates(start_date=start_date, end_date=end_date)
        df = rs.get_data()
        df = df.loc[df['is_trading_day'] == '1']
        return df

    # noinspection PyMethodMayBeStatic
    def query_all_stock(self) -> pandas.DataFrame:
        """
        查询所有股票
        :return
            返回的列：
                code        : str, 股票编码(例如：sh.000001)
                number      : str, 六位数字代码(例如：600810)
                exchange    : StockExchange, 交易所
                market      : StockMarket, 股票市场
                quality     : StockQuality, 股票品质
                name        : 证券名称(不带 ST 或 *ST)
                full_name   : 证券全名(带 ST 或 *ST)
        """
        # 获取所有股票信息
        latest_trade_day = self.get_latest_trade_date()
        rs = baostock.query_all_stock(day=latest_trade_day)
        df = rs.get_data()
        if len(df) == 0:
            return df

        # 整理数据
        df['number'] = df.apply(lambda x: self.get_stock_number(x['code']), axis=1)
        df['exchange'] = df.apply(lambda x: self.get_stock_exchange(x['code']), axis=1)
        df['market'] = df.apply(lambda x: self.get_stock_market(x['exchange'], x['number']), axis=1)
        df['full_name'] = df['code_name']
        df['name'] = df.apply(lambda x: self.get_stock_name(x['full_name']), axis=1)
        df['quality'] = df.apply(lambda x: self.get_stock_quality(x['full_name']), axis=1)
        df = df[['code', 'number', 'exchange', 'market', 'quality', 'name', 'full_name']]
        return df

    # noinspection PyMethodMayBeStatic
    def query_bars(self, code: str, start_date: str = daily_bar_first_date, end_date: str = None,
                   freq: StockBarFreq = StockBarFreq.day, fq: StockBarFQ = StockBarFQ.none) -> pandas.DataFrame:
        """
        获取历史A股K线数据
        :param code: str, 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。
        :param start_date: str, 开始日期（包含），格式“%Y-%m-%d”，为空时取2015-01-01；
        :param end_date: str, 结束日期（包含），格式“%Y-%m-%d”，为空时取最近一个交易日；
        :param freq: StockBarFreq, K线周期
        :param fq: StockBarFQ, 复权类型
        :return:
            返回如下列：
                code        str                 股票代码
                slot        datetime.datetime   时间槽(后置，例如：2020-01-02 10:35是指 10:30 - 10:35)
                open        float               开盘价
                high        float               最高价
                low         float               最低价
                close       float               收盘价
                volume      float               成交量
                amount      float               成交额
                change      float               涨幅%
                amplitude   float               振幅%
                kind        BarKind             K线类型(阴线、十字星、阳线)
                real_kind   BarKind             K线真实类型(阴线、十字星、阳线)
                turn        float               换手率%(分钟K线无换手率，值为0)
                fq          BarFQ               复权方式
        """
        # ----- 获取数据 ----- #
        # K线周期参数
        if freq == StockBarFreq.day:
            fields = 'date,       code, open, high, low, close, volume, amount, adjustflag, turn, pctChg'
        elif freq in [StockBarFreq.week, StockBarFreq.month]:
            fields = 'date,       code, open, high, low, close, volume, amount, adjustflag, turn, pctChg'
        else:
            fields = 'date, time, code, open, high, low, close, volume, amount, adjustflag'

        # 复权参数 1: 后复权; 2: 前复权; 3: 不复权;
        if fq == StockBarFQ.before:
            adjustflag = '2'
        elif fq == StockBarFQ.after:
            adjustflag = '1'
        else:
            adjustflag = '3'

        # 获取数据
        rs = baostock.query_history_k_data_plus(code=code, fields=fields, start_date=start_date, end_date=end_date,
                                                frequency=freq.value, adjustflag=adjustflag)
        df = rs.get_data()
        if len(df) == 0:
            return df

        # ----- 整理数据 ----- #
        def to_float(s: str) -> float:
            try:
                ret = float(s)
            except ValueError:
                ret = 0
            return ret

        # slot (date -> 2020-01-02; time -> 20200102110000000)
        if is_col_exists(df, 'time'):
            df['slot'] = df.apply(lambda x: str_to_date(x['time'][0:12], '%Y%m%d%H%M'), axis=1)
        else:
            df['slot'] = df.apply(lambda x: str_to_date(x['date']), axis=1)
        df['open'] = df.apply(lambda x: to_float(x['open']), axis=1)
        df['high'] = df.apply(lambda x: to_float(x['high']), axis=1)
        df['low'] = df.apply(lambda x: to_float(x['low']), axis=1)
        df['close'] = df.apply(lambda x: to_float(x['close']), axis=1)
        df['volume'] = df.apply(lambda x: to_float(x['volume']), axis=1)
        df['amount'] = df.apply(lambda x: to_float(x['amount']), axis=1)
        df['change'] = df.apply(lambda x: to_float(x['pctChg']), axis=1)  # %
        df['amplitude'] = (df['high'] - df['low']) / df['close'].shift() * 100
        df = add_col_kind(df)
        df = add_col_real_kind(df)
        if is_col_exists(df, 'turn'):  # %
            df['turn'] = df.apply(lambda x: to_float(x['turn']), axis=1)
        else:
            df['turn'] = 0
        df['fq'] = df.apply(lambda x: StockBarFQ(int(x['adjustflag'])), axis=1)

        # 指定输出的列
        df = df[['code', 'slot', 'open', 'high', 'low', 'close', 'volume', 'amount', 'change', 'amplitude', 'kind',
                 'real_kind', 'turn', 'fq']]
        return df

    # noinspection PyMethodMayBeStatic
    def get_stock_number(self, code: str) -> str:
        """
        根据股票代码，获取股票六位数字代码
        :param code: 股票代码(例如：sh.600810)
        :return: 股票六位数字代码
        """
        ret = code.split('.')[1]
        return ret

    # noinspection PyMethodMayBeStatic
    def get_stock_exchange(self, code: str) -> StockExchange:
        """
        根据股票代码，获取交易所
        :param code: 股票代码(例如：sh.600810)
        :return: 交易所(StockExchange)
        """
        ret = code.split('.')[0]
        if ret == 'sh':
            return StockExchange.sh
        elif ret == 'sz':
            return StockExchange.sz
        else:
            raise Exception('获取股票交易所失败！')

    # noinspection PyMethodMayBeStatic
    def get_stock_market_simple(self, code: str) -> StockMarket:
        """
        根据股票代码，获取股票市场
        :param code: 股票代码(例如：sh.600810)
        :return: 股票市场(StockMarket)
        """
        number = self.get_stock_number(code=code)
        exchange = self.get_stock_exchange(code=code)
        ret = self.get_stock_market(exchange=exchange, number=number)
        return ret

    # noinspection PyMethodMayBeStatic
    def get_stock_market(self, exchange: StockExchange, number: str) -> StockMarket:
        """
        根据股票六位数字代码，获取股票市场
            (exchange == StockExchange.sh) and (数字代码000打头) -> 上指
            (exchange == StockExchange.sh) and (数字代码 60打头) -> 上股(上海主板)
            (exchange == StockExchange.sh) and (数字代码688打头) -> 科创板
            (exchange == StockExchange.sz) and (数字代码399打头) -> 深指
            (exchange == StockExchange.sz) and (数字代码000、001、003打头) -> 深股(深圳主板)
            (exchange == StockExchange.sz) and (数字代码002打头) -> 中小板
            (exchange == StockExchange.sz) and (数字代码300打头) -> 创业板
        :param exchange: 交易所
        :param number: 股票六位数字代码(例如：600810)
        :return: 股票市场(StockExchange)
        """
        if (exchange == StockExchange.sh) and number.startswith('000'):
            return StockMarket.sh_index
        elif (exchange == StockExchange.sh) and number.startswith('60'):
            return StockMarket.sh_stock
        elif (exchange == StockExchange.sh) and number.startswith('688'):
            return StockMarket.sh_sti
        elif (exchange == StockExchange.sz) and number.startswith('399'):
            return StockMarket.sz_index
        elif (exchange == StockExchange.sz) and (
                number.startswith('000') or number.startswith('001') or number.startswith('003')):
            return StockMarket.sz_stock
        elif (exchange == StockExchange.sz) and number.startswith('002'):
            return StockMarket.sz_sme
        elif (exchange == StockExchange.sz) and number.startswith('300'):
            return StockMarket.sz_gem
        else:
            print(exchange, number)
            raise Exception('获取股票市场失败！')

    # noinspection PyMethodMayBeStatic
    def get_stock_name(self, full_name: str) -> str:
        """
        根据股票全称，获取股票名称(去掉打头的ST和*ST)
        :param full_name: 股票全称
        :return: 股票名称
            例如：
                full_name       返回
                新湖中宝        新湖中宝
                ST罗顿         罗顿
                *ST山水        山水
        """
        ret = full_name
        ret = ret.lstrip('*ST')
        ret = ret.lstrip('ST')
        return ret

    # noinspection PyMethodMayBeStatic
    def get_stock_quality(self, full_name: str) -> StockQuality:
        """
        根据股票全称，获取股票品质
        :param full_name: 股票全称
        :return: 股票品质(StockQuality)
        """
        if full_name.startswith('*ST'):
            return StockQuality.st_plus
        if full_name.startswith('ST'):
            return StockQuality.st
        return StockQuality.normal
