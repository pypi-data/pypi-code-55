# -*- coding: utf-8 -*-
from iqsopenapi.basicdata  import *
from iqsopenapi.core  import *
from iqsopenapi.marketdata  import *
from iqsopenapi.models  import *
from iqsopenapi.trade  import *
from iqsopenapi.util  import *
from iqsopenapi.external import *

def run_file(strategy_file_path, config=None):
    """执行文件"""

    loader = FileStrategyLoader(strategy_file_path)
    return __run(config,loader)

def run_code(source_code, config=None):
    """执行源代码"""

    loader = SourceCodeStrategyLoader(source_code)
    return __run(config,loader)


def run_func(**kwargs):
    """执行自定义函数"""

    config = kwargs.get('config', kwargs.get('__config__', None))
    user_funcs = {
        k: kwargs[k]
        for k in ['on_init', 'on_bar', 'on_tick','on_order','on_trade','on_open','on_close']
        if k in kwargs
    }

    loader = UserFuncStrategyLoader(user_funcs)
    return __run(config,loader)

def __run(config, strategy_loader):
    try:
        environment = Environment(config)
        if environment.config.log:
            logger.setLevel(environment.config.log['level'])
            logutil.log2file(environment.config.log['file'])

        ucontext = StrategyContext()

        event_bus = EventBus()

        environment.scheduler = Scheduler(event_bus)

        environment.market_api = MarketApi(event_bus)

        environment.market_api.Init()

        environment.basicdata_api = BasicDataApi()

        if environment.config.run_type == 'PAPER_TRADING':
            environment.trade_api = PaperTradeApi(event_bus)
            environment.trade_api.Init()
        elif environment.config.run_type == 'LIVE_TRADING':
            environment.trade_api = RealTradeApi(event_bus)
            environment.trade_api.Init()
        elif environment.config.run_type == 'BACKTEST':
            raise Exception('BACKTEST is not support!')

        if environment.config.ext_notify:
            user_notify = ExternalNotify(environment.config.ext_notify['address'],event_bus)
            user_notify.init()
        from copy import copy

        scope = copy(iqsopenapi.models.__dict__)
        scope.update(iqsopenapi.core.StrategyContext.__dict__)

        strategy_loader.load(scope)

        user_strategy = Strategy(event_bus, scope, ucontext)

        user_strategy.init()    

        event_bus.start()

        return True
    except Exception as e:
        logger.error('init exception',e)
        return False
