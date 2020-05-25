# -*- coding: utf-8 -*-
from enum import IntEnum

class TradeCounterType(IntEnum):
    ''' 柜台类型 '''

    ''' 默认-无 '''
    NONE=0
    ''' CTP '''
    CTP = 1
    ''' 恒生 '''
    HS = 2
    ''' 顶点 '''
    DD = 3
    ''' 金仕达 '''
    JSD = 4
    ''' 飞马 '''
    FM = 5
    
class ConOrderTimeValidTypeEnum(IntEnum):
    ''' 条件单查询日期类型 '''

    ''' 当前交易日有效 '''
    CurrentTradingDayValid=-1
    ''' 永久有效 '''
    ForverValid=0