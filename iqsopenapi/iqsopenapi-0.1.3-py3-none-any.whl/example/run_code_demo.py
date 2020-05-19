# -*- coding: utf-8 -*-

from iqsopenapi import *
import json

code = """
from iqsopenapi import *

def on_init(ctx):
    logger.info("init")
    ctx.subscribe(('rb2010.SHFE','TICK'),('IH2005.CFFEX','3m'))

def on_tick(ctx,tick):
    logger.info('tick:{0},{1},{2}'.format(tick.symbol,tick.local_time,tick.last))
"""

config = """
{
    "runtime":"DEBUG",
    "run_type":"PAPER_TRADING",
    "acct_info":{
            "strategy_id":"21",
            "account":"10030"
        }
}
"""

js = json.loads(config,encoding='utf-8')
run_code(code,js)