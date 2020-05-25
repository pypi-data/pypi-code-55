# -*- coding: utf-8 -*-

from iqsopenapi.core.events import *
from iqsopenapi.environment import Environment
from iqsopenapi.core.Scheduler import *
import datetime

class Strategy(object):
    def __init__(self, event_bus,scope, ucontext):
        self.__user_context = ucontext
        self.__event_bus = event_bus
        self.__init = scope.get('on_init', None)
        self.__handle_bar = scope.get('on_bar', None)
        self.__handle_tick = scope.get('on_tick', None)
        self.__handle_order = scope.get('on_order', None)
        self.__handle_trade = scope.get('on_trade', None)
        self.__handle_open = scope.get('on_open', None)
        self.__handle_close = scope.get('on_close', None)

        if self.__init is not None:
            event_bus.add_listener(EVENT.On_Init, self.init)
        if self.__handle_tick is not None:
            event_bus.add_listener(EVENT.On_Tick, self.handle_tick)
        if self.__handle_bar is not None:
            event_bus.add_listener(EVENT.On_Bar, self.handle_bar)
        if self.__handle_order is not None:
            event_bus.add_listener(EVENT.On_Order, self.handle_order)
        if self.__handle_trade is not None:
            event_bus.add_listener(EVENT.On_Trade, self.handle_trade)
        if self.__handle_open is not None:
            Environment.get_instance().scheduler.add_task(SchedulerTask(None,datetime.time(20,30),EVENT.On_Open))
            event_bus.add_listener(EVENT.On_Open, self.handle_open)
        if self.__handle_close is not None:
            Environment.get_instance().scheduler.add_task(SchedulerTask(None,datetime.time(15,30),EVENT.On_Close))
            event_bus.add_listener(EVENT.On_Close, self.handle_close)
        event_bus.add_listener(EVENT.On_Scheduler, self.handle_scheduler)
        
    def user_context(self):
        return self.__user_context

    def init(self):
        logger.info("begin init")
        self.__init(self.__user_context)
        logger.info("init complated")

    def handle_bar(self, event):
        self.__rebuild_event_data(event.data)
        self.__handle_bar(self.__user_context, event.data)

    def handle_tick(self, event):
        self.__rebuild_event_data(event.data)
        self.__handle_tick(self.__user_context, event.data)

    def handle_order(self, event):
        self.__rebuild_event_data(event.data)
        self.__handle_order(self.__user_context, event.data)

    def handle_trade(self, event):
        self.__rebuild_event_data(event.data)
        self.__handle_trade(self.__user_context, event.data)

    def __rebuild_event_data(self, event_data):
        if event_data is None:
            return
        if hasattr(event_data,'symbol') and '.' not in event_data.symbol:
                event_data.symbol = '{0}.{1}'.format(event_data.symbol, event_data.exchange.name)

    def handle_open(self, event):
        if event is None or event.raise_time is None:
            return
        begin = event.raise_time
        end = begin + datetime.timedelta(days=1)
        open_times = Environment.get_instance().basicdata_api.GetOpenTimes(begin,end)
        if open_times is None or len(open_times) <= 0:
            return
        raise_time = event.raise_time + datetime.timedelta(hours=13)
        for x in open_times:
            if raise_time >= datetime.datetime.strptime(x.begin,'%Y%m%d%H%M%S') and raise_time <= datetime.datetime.strptime(x.end,'%Y%m%d%H%M%S'):
                logger.info("begin on_open")
                self.__handle_open(self.__user_context)
                logger.info("on_open complated")
                return

    def handle_close(self, event):
        if event is None or event.raise_time is None:
            return
        begin = event.raise_time + datetime.timedelta(days=-1)
        end = event.raise_time
        open_times = Environment.get_instance().basicdata_api.GetOpenTimes(begin,end)
        if open_times is None or len(open_times) <= 0:
            return
        raise_time = event.raise_time + datetime.timedelta(hours=-1)
        for x in open_times:
            if raise_time >= datetime.datetime.strptime(x.begin,'%Y%m%d%H%M%S') and raise_time <= datetime.datetime.strptime(x.end,'%Y%m%d%H%M%S'):
                logger.info("begin on_close")
                self.__handle_close(self.__user_context)
                logger.info("on_close complated")
                return

    def handle_scheduler(self, event):
        if event is None or event.func is None:
            return
        event.func(*event.args)

if __name__ == '__main__':

    from iqsopenapi import *
    from iqsopenapi.core import *

    ucontext = StrategyContext()

    event_bus = EventBus()

    loader = FileStrategyLoader(r'D:\gitwork\inquantstudio\IQSOpenApi\IQS.OpenApi.Python\iqsopenapi\example\teststrategy.py')

    from copy import copy

    scope = copy(iqsopenapi.__dict__)

    loader.load(scope)

    user_strategy = Strategy(event_bus, scope, ucontext)

    user_strategy.init()    

    marketApi = MarketApi(event_bus)

    marketApi.Init()

    event_bus.start()

    ret1 = marketApi.Subscribe("rb2010.SHFE.TICK.0","rb2010.SHFE.BAR.300","rb2005.SHFE.TICK.0")

    pass