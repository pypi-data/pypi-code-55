# -*- coding: utf-8 -*-


class BarData(object):
    """bar数据，参考zipline._protocol.BarData"""
    @property
    def current_kline_date(self):
        return self._current_kline_date

    def __init__(self):
        self._current_kline_date = None   # e.g. "2019-07-24"

    def do_init(self, stock_type):
        self._stock_type = stock_type  # e.g. 'HK', 'US', 'ASHARE'

    def set_current_kline_date(self, current_kline_date):
        self._current_kline_date = current_kline_date

    def can_trade(self, security_code):
        """
        当前bar能否交易
        :param security_code: 交易标的 e.g. "00700.HK"
        :param kline_date: bar日期 e.g. "2019-07-24"
        :return:
        """
        return True

    def current(self, security_code_list, kline_date_list=None, select_column_clause=None, table_name=None, enable_print_sql=False):
        """
        获取当前bar的itemView信息，重试10次
        :param security_code_list, e.g. ["00700.HK","01800.HK]
        :param kline_date_list: bar日期 e.g. ["2019-07-24"]
        :param select_column_clause e.g. "trade_date,security_code,hfq_close as close"
        :param enable_print_sql 是否打印sql
        :return: bar_item e.g. {"security_code": "00700.HK", "close": 1.0, "kline_date": "2019-07-24"}
        """
        pass

    def calc_lot_size(self, security_code):
        """一手股票的股数, 美股为1，A股为100，港股中每手的股数不同"""
        if ".HK" in security_code:
            return 100
        elif ".SZ" in security_code or ".SH" in security_code:
            return 100
        else:
            return 1

    def can_buy_lot(self, cash, lot_size, price:float, min_move, commision):
        """
        计算当前金额可以买多少股票
        假设条件：1）当前腾讯股价为100CNY/股，2）有最小买入单位“手”=100股
        此时已经确定的逻辑：腾讯一手价值10000CNY，最多能持有19手（19手价值190000CNY<20万CNY，20手价值200000CNY=20万CNY，但是因为有手续费，所以不能采纳），手续费标准为千一，实际为190CNY。
        则完成该仓位时，分配给腾讯的仓位应该为19手腾讯（股票）+（10000-190）CNY现金。
        :param cash: e.g. 20万
        :param lot_size: e.g. 100
        :param price: e.g. 100
        :param min_move: e.g. 0
        :param commision: e.g. 0.001
        :return:
        """
        # return self._calc_trade_lot(cash / (price + min_move + commision), lot_size) # 这里是zipline的逻辑
        return self._calc_trade_lot(cash / (price + min_move + price*commision), lot_size) # 这里改为和position计算balance_cash的逻辑一致

    def _calc_trade_lot(self, trade_lot:int, lot_size:int=1):
        """
        把计划交易的股数转成可以被手数整除的实际股数
        :param trade_lot 计划交易的股数，可以为float类型的值
        :param lot_size 1手多少股
        """
        # if trade_lot <= lot_size:  # 如果数量小于1手，就下1手的数量
        #     return lot_size
        if trade_lot <= lot_size:  # 如果数量小于1手，就下0手的数量
            return 0
        if trade_lot % lot_size == 0:  # 刚好整除就下trade_lot数量，否则向下取整
            return trade_lot
        else:
            return int(trade_lot / lot_size) * lot_size


