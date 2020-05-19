from iqsopenapi import *


def init(context):
    logger.info("init")
    
def handle_tick(context,tick):
    logger.info('from file tick:{0},{1},{2}'.format(tick.Symbol,tick.LocalTime,tick.LastPx))

def handle_bar(context, bar):
    logger.info('bar:{0},{1},{2}'.format(bar.Symbol,bar.LocalTime,bar.LastPx))
