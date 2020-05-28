# -*- coding: utf-8 -*-

from iqsopenapi import *


def init(context):
    logger.info("init")
    context.s1 = "rb2010.SHFE"

def handle_tick(context,tick):
    logger.info('from func tick:{0},{1},{2}'.format(tick.Symbol,tick.LocalTime,tick.LastPx))

def handle_bar(context, bar):
    logger.info('from func bar:{0},{1},{2}'.format(bar.Symbol,bar.LocalTime,bar.LastPx))


config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

# 您可以指定您要传递的参数
run_func(init=init, handle_tick=handle_tick, handle_bar=handle_bar, config=config)
