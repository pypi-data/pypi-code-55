# -*- coding: utf-8 -*-
from iqsopenapi.environment import Environment
from iqsopenapi.models import *
from iqsopenapi.core.Scheduler import *
from collections import defaultdict
from copy import copy

class StrategyContext(object):
    """
    策略上下文
    """
    def __init__(self):
        """初始化"""
        pass

    def get_strategy_id(self):
        """获取策略编号"""
        if Environment.get_instance().config is None or Environment.get_instance().config.acct_info is None:
            return None
        return Environment.get_instance().config.acct_info['strategy_id']
   
    def subscribe(self,*args):
        """行情订阅"""

        subs = []
        for arg in args:
            if arg[1].upper() == "TICK":
                sub = '{0}.TICK.0'.format(arg[0])
                subs.append(sub)
            else:
                bar_type = self.__get_bar_type(arg[1])
                sub = '{0}.BAR.{1}'.format(arg[0],bar_type)
                subs.append(sub)
        return Environment.get_instance().market_api.Subscribe(*subs)

    def unsubscribe(self,*args):
        """取消订阅"""

        subs = []
        for arg in args:
            if arg[1].upper() == "TICK":
                sub = '{0}.TICK.0'.format(arg[0])
                subs.append(sub)
            else:
                bar_type = self.__get_bar_type(arg[1])
                sub = '{0}.BAR.{1}'.format(arg[0],bar_type)
                subs.append(sub)
        return Environment.get_instance().market_api.Unsubscribe(*subs)

    def get_subscribelist(self):
        """获取订阅列表"""
        return Environment.get_instance().market_api.GetSubscibes()

    def get_contract(self, symbol):
        """获取合约信息"""
        (code,exchange) = self.__split_symbol(symbol)
        data = Environment.get_instance().basicdata_api.GetContract(code, exchange)
        self.__rebuild_data(data)
        return data

    def get_dominant_contract(self, variety):
        """获取主力合约"""
        data = Environment.get_instance().basicdata_api.GetMainContract(variety)
        self.__rebuild_data(data)
        return data

    def get_last_ticks(self, symbol, count):
        """获取最近几笔tick"""
        (code,exchange) = self.__split_symbol(symbol)
        data = Environment.get_instance().market_api.GetLastTick(code, exchange, count)
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_last_bars(self, symbol, barType, count):
        """获取最近几笔bar"""
        (code,exchange) = self.__split_symbol(symbol)
        bar_type = self.__get_bar_type(barType)
        data = Environment.get_instance().market_api.GetLastBar(code, exchange, bar_type, count)
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_history_bars(self, symbol, barType, startTime, endTime):
        """获取历史bar"""
        (code,exchange) = self.__split_symbol(symbol)
        bar_type = self.__get_bar_type(barType)
        start = startTime
        end = endTime
        if(isinstance(startTime,datetime.datetime)):
            start = startTime.strftime("%Y%m%d%H%M%S")
            end = endTime.strftime("%Y%m%d%H%M%S")
        elif(isinstance(startTime,datetime.date)):
            start = startTime.strftime("%Y%m%d")
            end = endTime.strftime("%Y%m%d")
        data = Environment.get_instance().market_api.GetHisBar(code, exchange, bar_type, start, end)
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_history_ticks(self, symbol, startTime, endTime):
        """获取订阅列表"""
        (code,exchange) = self.__split_symbol(symbol)
        start = startTime
        end = endTime
        if(isinstance(startTime,datetime.datetime)):
            start = startTime.strftime("%Y%m%d%H%M%S")
            end = endTime.strftime("%Y%m%d%H%M%S")
        elif(isinstance(startTime,datetime.date)):
            start = startTime.strftime("%Y%m%d")
            end = endTime.strftime("%Y%m%d")
        data = Environment.get_instance().market_api.GetHisTick(code, exchange, start, end)
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def insert_order(self, symbol, order_side, order_type, offset, price, quantity):
        """下单"""
        (code,exchange) = self.__split_symbol(symbol)
        data = Environment.get_instance().trade_api.SendOrder(code,exchange,order_side,price,quantity,order_type,offset)
        self.__rebuild_data(data)
        return data

    def insert_smart_order(self, symbol, quantity, price=None, today_first=True):
        """智能报单
        symbol—合约代码, str
        quantity—委托手数，正值表示买入，负值表示卖出, int
        当前多仓，正数：开多仓
        当前多仓，负数：平多仓，超过头寸数量反方向开空仓
        当前空仓，正数：平空仓，超过头寸数量反方向开多仓
        当前空仓，负数：开空仓

        当前存在双向单，正数：平空仓，超过空头头寸数量开多仓
        当前存在双向单，负数：平多仓，超过多头头寸数量开空仓

        price—委托价格，None表示市价单，否则为限价单, float
        today_first—平仓优先级，默认优先平今仓，超出部分平老仓
        """
        if quantity == 0:
            raise Exception('smart order quantity must not be less than 0!')
        order_type = OrderType.LMT
        if price is None:
            price = 0.0
            order_type = OrderType.MKT  
        pos = self.__get_smart_order_pos(symbol,quantity)
        if pos is None:
            if quantity > 0:
                return self.insert_order(symbol,OrderSide.Buy,order_type,Offset.Open,price,quantity)
            else:
                return self.insert_order(symbol,OrderSide.Sell,order_type,Offset.Open,price,-quantity)
        if pos.side == PosSide.Net:
            raise Exception('smart order only support long or short position!')
        if pos.side == PosSide.Long and quantity > 0:
            return self.insert_order(symbol,OrderSide.Buy,order_type,Offset.Open,price,quantity)
        elif pos.side == PosSide.Long and quantity < 0:
            closeQty = min(pos.quantity,-quantity)
            order = None
            if today_first:
                if pos.today_qty > 0:
                    order = self.insert_order(symbol,OrderSide.Sell,order_type,Offset.CloseToday,price,min(closeQty,pos.today_qty))
                closeYesQty = closeQty - min(closeQty,pos.today_qty)
                if closeYesQty > 0:
                    order = self.insert_order(symbol,OrderSide.Sell,order_type,Offset.CloseYesterday,price,closeYesQty)
            else:
                yesQty = pos.quantity - pos.today_qty
                if yesQty > 0:
                    order = self.insert_order(symbol,OrderSide.Sell,order_type,Offset.CloseYesterday,price,min(closeQty,yesQty))
                closeTodayQty = closeQty - min(closeQty,yesQty)
                if closeTodayQty > 0:
                    order = self.insert_order(symbol,OrderSide.Sell,order_type,Offset.CloseToday,price,closeTodayQty)
            if -quantity - closeQty > 0:
                return self.insert_order(symbol,OrderSide.Sell,order_type,Offset.Open,price,-quantity - closeQty)
            else:
                return order
        elif pos.side == PosSide.Short and quantity > 0:
            closeQty = min(pos.quantity,quantity)
            order = None
            if today_first:
                if pos.today_qty > 0:
                    order = self.insert_order(symbol,OrderSide.Buy,order_type,Offset.CloseToday,price,min(closeQty,pos.today_qty))
                closeYesQty = closeQty - min(closeQty,pos.today_qty)
                if closeYesQty > 0:
                    order = self.insert_order(symbol,OrderSide.Buy,order_type,Offset.CloseYesterday,price,closeYesQty)
            else:
                yesQty = pos.quantity - pos.today_qty
                if yesQty > 0:
                    order = self.insert_order(symbol,OrderSide.Buy,order_type,Offset.CloseYesterday,price,min(closeQty,yesQty))
                closeTodayQty = closeQty - min(closeQty,yesQty)
                if closeTodayQty > 0:
                    order = self.insert_order(symbol,OrderSide.Buy,order_type,Offset.CloseToday,price,closeTodayQty)
            if quantity - closeQty > 0:
                return self.insert_order(symbol,OrderSide.Buy,order_type,Offset.Open,price,quantity - closeQty)
            else:
                return order
        elif pos.side == PosSide.Short and quantity < 0:
            return self.insert_order(symbol,OrderSide.Sell,order_type,Offset.Open,price,-quantity)

        raise Exception('smart order error!')

    def __get_smart_order_pos(self,symbol, quantity):
        '''获取智能单持仓'''
        all_pos = self.get_positions()
        if symbol not in all_pos:
             return None
        if len(all_pos[symbol]) >= 2:
            if quantity > 0:
                if PosSide.Short in all_pos[symbol]:
                    return all_pos[symbol][PosSide.Short]
                raise Exception('smart order not exist short position!')
            elif quantity < 0:
                if PosSide.Long in all_pos[symbol]:
                    return all_pos[symbol][PosSide.Long]
                raise Exception('smart order not exist long position!')
            else:
                raise Exception('smart order quantity must not be less than 0!')
        else:
            return list(all_pos[symbol].values())[0]

    def cancel_order(self, order):
        """撤单"""
        data = Environment.get_instance().trade_api.CancelOrder(order)
        self.__rebuild_data(data)
        return data

    def get_orders(self):
        """获取当日委托"""
        data = Environment.get_instance().trade_api.GetOrders()
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_trades(self):
        """获取当日成交"""
        data = Environment.get_instance().trade_api.GetTrades()
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_order(self, order_id):
        """获取当日委托"""
        data = Environment.get_instance().trade_api.GetOrder(order_id)
        self.__rebuild_data(data)
        return data

    def get_open_orders(self):
        """获取Open委托"""
        data = Environment.get_instance().trade_api.GetOpenOrders()
        if not data:
            return data
        self.__rebuild_data(*data)
        return data

    def get_positions(self):
        """获取持仓"""
        data = Environment.get_instance().trade_api.GetPositions()
        if not data:
            return defaultdict(dict)
        self.__rebuild_data(*data)
        val = defaultdict(dict)
        for x in data:
            val[x.symbol][x.side] = x
        return dict(val)

    def get_position(self, symbol):
        """获取持仓"""
        all_pos = self.get_positions()
        if symbol not in all_pos:
             return {PosSide.Long:None,PosSide.Short:None}
        val = copy(all_pos[symbol])
        if PosSide.Long not in val:
            val[PosSide.Long] = None
            return val
        if PosSide.Short not in val:
            val[PosSide.Short] = None
            return val
        return val

    def get_account(self):
        """获取订阅列表"""
        return Environment.get_instance().trade_api.GetAccount()

    def run_by_time(self,func,time,*args):
        """定时运行函数"""
        return Environment.get_instance().scheduler.add_task(SchedulerTask(func,time,EVENT.On_Scheduler,args))

    def insert_func_at_time(self,func,time,*args):
        """指定时间运行函数"""
        return Environment.get_instance().scheduler.add_task(SchedulerTask(func,time,EVENT.On_Scheduler,args))

    def get_datetime(self):
        """获取当前时间"""
        return datetime.datetime.now()

    def __split_symbol(self,symbol):
        if symbol is None or symbol == '':
            raise Exception('illegal symbol:' + symbol)
        arr = symbol.split('.')
        if len(arr) != 2:
            raise Exception('illegal symbol:' + symbol)
        return (arr[0],Exchange[arr[1]])

    def __get_bar_type(self,bartype):
        if bartype is None or bartype == '':
            raise Exception('illegal bartype:' + bartype)
        if bartype.isdigit():
            return bartype
        multi = int(bartype[:-1])
        unit = 0
        if bartype[-1] == 's':
            unit = 1
        elif bartype[-1] == 'm':
            unit = 60
        elif bartype[-1] == 'h':
            unit = 3600
        elif bartype[-1] == 'd':
            unit = 86400
        else:
            raise Exception('illegal bartype:' + bartype)
        return multi * unit

    def __rebuild_data(self, *data):
        if data is None:
            return
        for x in data:
            if hasattr(x,'symbol') and '.' not in x.symbol:
                x.symbol = '{0}.{1}'.format(x.symbol, x.exchange.name)