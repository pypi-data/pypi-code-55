# -*- coding: utf-8 -*-
import numpy as np
from iqsopenapi import *
import datetime

def on_init(ctx):
    #variables
    ctx.f1 = 5
    ctx.f2 = 0.2
    ctx.f3 = 0.2
    ctx.bet_size = 0.1
    ctx.symbol = 'rb'
    ctx.domi_contract = None
    ctx.last_domi = None

    id = ctx.get_strategy_id()

    ctx.subscribe(('rb2010.SHFE','1m'),('jd2009.CFFEX','3m'))

    ctx.domi_contract = ctx.get_dominant_contract(ctx.symbol)
    conInfo = ctx.get_contract(ctx.domi_contract.symbol)

    last_bars = ctx.get_last_bars(ctx.domi_contract.symbol,'1d',300)

    last_ticks = ctx.get_last_ticks(ctx.domi_contract.symbol,100)

    account = ctx.get_account()

    orders = ctx.get_open_orders()

    positions = ctx.get_positions()

    trades = ctx.get_trades()

    order = ctx.insert_order('rb2010.SHFE',OrderSide.Buy,OrderType.MKT,Offset.Open,0,3)

    #order1 = ctx.cancel_order(order)

    order2 = ctx.get_order(order.order_id)

    bars1 = ctx.get_history_bars('rb2010.SHFE','1m','20200521','20200522')

    bars2 = ctx.get_history_bars('rb2010.SHFE','1m',datetime(2020,5,21,9,10,0),datetime(2020,5,21,11,10,0))

    bars2 = ctx.get_history_bars('rb2010.SHFE','1m',date(2020,5,21),date(2020,5,22))
    
    ctx.run_by_time(run_time,datetime(2020,5,21,13,58,0),'CCC','DDDDD')

    ctx.run_by_time(run_time,time(13,50,0))

    ctx.insert_func_at_time(run_time,time(13,49,0))

    ctx.insert_func_at_time(run_time,datetime(2020,5,21,14,10,0),'AAA','BBBB')

    pass

def run_time(*args):
    pass
    
def on_open(ctx):
    ctx.domi_contract = ctx.get_dominant_contract(ctx.symbol)
    conInfo = ctx.get_contract(ctx.domi_contract.symbol)
    ctx.lots = conInfo.lots
    ctx.step = conInfo.step
    ctx.subscribe((ctx.domi_contract,'1m'))
    ctx.range = cal_range(ctx)
    ctx.prepared = False
    
def on_close(ctx):
    ctx.last_domi = ctx.domi_contract
    
def cal_range(ctx):
    last_bars = ctx.get_last_bars(ctx.domi_contract,'1d',300)
    High = np.array([bar.high for bar in last_bars])
    Low = np.array([bar.low for bar in last_bars])
    Close = np.array([bar.close for bar in last_bars])
    Range = talib.ATR(High,Low,Close,timeperiod=ctx.f1 - 1)[-1]
    return Range
    
def change_contract(ctx):
    lp = ctx.get_position(ctx.last_domi)
    quantity = (lp.quantity - lp.frozen) * lp.OrderSide
    if quantity:
        ctx.insert_smart_order(ctx.last_domi,-quantity)
        ctx.insert_smart_order(ctx.domi_contract,quantity)
        ctx.unsubscribe((ctx.last_domi,'1m'))

def on_tick(ctx,tick):
    logger.info('tick:{0},{1},{2}'.format(tick.symbol,tick.local_time,tick.last))

def on_order(ctx,order):
    logger.info('on order:{0},{1},{2},{3}'.format(order.symbol,order.side.name,order.offset.name,order.status.name))

def on_trade(ctx,trade):
    logger.info('on trade:{0},{1},{2},{3},{4}'.format(trade.symbol,trade.side.name,trade.offset.name,trade.quantity,trade.price))
    
def on_bar(ctx,bar):
    logger.info('bar:{0},{1},{2}'.format(bar.symbol,bar.local_time,bar.close))
    #if bar.symbol != ctx.domi_contract: return
    #if not ctx.prepared:
    #    if ctx.domi_contract != ctx.last_domi and ctx.last_domi:
    #        change_contract(ctx)
    #    ctx.open_price = bar.open
    #    ctx.up = ctx.open_price + ctx.f2 * ctx.range
    #    ctx.down = ctx.open_price - ctx.f3 * ctx.range
    #    ctx.up = round(ctx.up / ctx.step) * ctx.step
    #    ctx.down = round(ctx.down / ctx.step) * ctx.step
    #    ctx.last_high = bar.high
    #    ctx.last_low = bar.low
    #    ctx.prepared = True
    #    return
    #else:
    #    if not (bar.high > ctx.up and bar.low < ctx.down):
    #        if ctx.last_high <= ctx.up and bar.open >= ctx.up:
    #            acc = ctx.get_account()
    #            quantity = int(acc.available / ctx.up / ctx.lots / 0.01 *
    #            ctx.bet_size)
    #            if quantity:
    #                ctx.insert_smart_order(ctx.domi_contract,quantity)
    #        if ctx.last_low >= ctx.down and bar.open <= ctx.down:
    #            acc = ctx.get_account()
    #            quantity = int(acc.available / ctx.up / ctx.lots / 0.01 *
    #            ctx.bet_size)
    #            if quantity:
    #                ctx.insert_smart_order(ctx.domi_contract,-quantity)
    #    ctx.last_high = bar.high
    #    ctx.last_low = bar.low
config = {
    "runtime":"DEBUG",
    "run_type":"LIVE_TRADING",
    "log":{
            'level':'INFO',
            'file' :r"D:\logs\test\strategy.log",
        },
    #"ext_notify":{
    #        "type":"websocket",
    #        "address":"ws://localhost:14002/"
    #    },
    #"acct_info":{
    #        "strategy_id":"21",
    #        "account":"10030"
    #    }
    "acct_info":{
            "strategy_id":"1021",
            "account":"060031",
            "password":"Wx@123456",
            "comp_counter": 96,
            "broker_type":152
        }
}
run_func(**globals())