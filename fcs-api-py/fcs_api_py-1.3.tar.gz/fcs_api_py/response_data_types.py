#OK
class r_currency_details:
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info
    
    class item_response():
        def __init__(self,short_name,name,country,code_n,subunit,website,symbol,bank,banknotes,coins,icon,type,symbol_2,banknotes_2,coins_2):
            self.short_name =short_name
            self.name = name
            self.country = country
            self.code_n = code_n
            self.subunit = subunit
            self.website = website
            self.symbol = symbol
            self.bank = bank
            self.banknotes = banknotes
            self.coins = coins
            self.icon = icon
            self.type = type
            self.symbol_2 = symbol_2
            self.banknotes_2 = banknotes_2
            self.coins_2 = coins_2

    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_list_symbols():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class item_response():
        def __init__(self, id, decimal, symbol):
            self.id = id
            self.decimal = decimal
            self.symbol = symbol
    
    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_currency_latest_price():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class item_response():
        def __init__(self, id, price, change, chg_per, last_changed, symbol):
            self.id = id
            self.price = price
            self.change = change
            self.chg_per = chg_per
            self.last_changed = last_changed
            self.symbol = symbol
    
    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_currency_converter():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class item_response():
        def __init__(self, price_1x_origin, price_1x_dest, total):
            self.id = id
            self.price_1x_origin = price_1x_origin
            self.price_1x_dest = price_1x_dest
            self.total = total

    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_base_currency():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class info:
        def __init__(self,base, type, server_time,credit_count):
            self.base = base
            self.type = type
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_currency_cross():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info
    
    class item_response():
        def __init__(self, id, price, change, chg_per, last_changed, type, symbol):
            self.id = id
            self.price = price
            self.change = change
            self.chg_per = chg_per
            self.last_changed = last_changed
            self.type = type
            self.symbol = symbol

    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_last_candle():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class item_response():
        def __init__(self, o, h, l, c, t, tm, symbol):
            self.o = o
            self.h = h
            self.l = l
            self.c = c
            self.t = t
            self.tm = tm
            self.symbol = symbol

    class info:
        def __init__(self,server_time,credit_count):
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_historical_price():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class item_response():
        def __init__(self, o, h, l, c, t, tm):
            self.o = o
            self.h = h
            self.l = l
            self.c = c
            self.t = t
            self.tm = tm

    class info:
        def __init__(self,id, decimal, symbol, period, server_time,credit_count):
            self.id = id
            self.decimal = decimal
            self.period = period
            self.symbol = symbol
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_pivot_points():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class response():
        def __init__(self,oa_summary, pivot_point):
            self.oa_summary = oa_summary
            self.pivot_point = pivot_point
    
    class pivot_point():
        def __init__(self, classic, fibonacci, camarilla, woodie, demark):
            self.classic = classic
            self.fibonacci = fibonacci
            self.camarilla = camarilla
            self.woodie = woodie
            self.demark = demark
    
    class classic():
        def __init__(self, pp, R1, R2, R3, S1, S2, S3):
            self.pp = pp
            self.R1 = R1
            self.R2 = R2
            self.R3 = R3
            self.S1 = S1
            self.S2 = S2
            self.S3 = S3
    
    class fibonacci():
        def __init__(self, pp, R1, R2, R3, S1, S2, S3):
            self.pp = pp
            self.R1 = R1
            self.R2 = R2
            self.R3 = R3
            self.S1 = S1
            self.S2 = S2
            self.S3 = S3
    
    class camarilla():
        def __init__(self, pp, R1, R2, R3, R4, S1, S2, S3, S4):
            self.pp = pp
            self.R1 = R1
            self.R2 = R2
            self.R3 = R3
            self.R4 = R4
            self.S1 = S1
            self.S2 = S2
            self.S3 = S3
            self.S4 = S4
    
    class woodie():
        def __init__(self, pp, R1, R2, S1, S2):
            self.pp = pp
            self.R1 = R1
            self.R2 = R2
            self.S1 = S1
            self.S2 = S2

    class demark():
        def __init__(self, high, low, R1, S1):
            self.high = high
            self.low = low
            self.R1 = R1
            self.S1 = S1
            
    class info:
        def __init__(self,id, decimal, symbol, period, disclaimer, update, update_time, server_time,credit_count):
            self.id = id
            self.decimal = decimal
            self.period = period
            self.symbol = symbol
            self.disclaimer = disclaimer
            self.update = update
            self.update_time = update_time
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_moving_average():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class response():
        def __init__(self,oa_summary, count, ma_avg):
            self.oa_summary = oa_summary
            self.count = count
            self.ma_avg = ma_avg

    class ma_avg():
        def __init__(self, SMA, EMA, summary):
            self.SMA = SMA
            self.EMA = EMA
            self.summary = summary
    
    class SMA():
        def __init__(self, MA5, MA10, MA20, MA50, MA100, MA200):
            self.MA5 = MA5
            self.MA10 = MA10
            self.MA20 = MA20
            self.MA50 = MA50
            self.MA100 = MA100
            self.MA200 = MA200
    
    class EMA():
        def __init__(self, MA5, MA10, MA20, MA50, MA100, MA200):
            self.MA5 = MA5
            self.MA10 = MA10
            self.MA20 = MA20
            self.MA50 = MA50
            self.MA100 = MA100
            self.MA200 = MA200

    class v_s():
        def __init__(self, v, s):
            self.v=v
            self.s=s

    class count():
        def __init__(self,Total_Buy, Total_Sell, Total_Neutral, maBuy, maSell):
            self.Total_Buy = Total_Buy
            self.Total_Sell = Total_Sell
            self.Total_Neutral = Total_Neutral
            self.maBuy = maBuy
            self.maSell = maSell

    class info:
        def __init__(self,id, decimal, symbol, period, disclaimer, update, update_time, server_time,credit_count):
            self.id = id
            self.decimal = decimal
            self.period = period
            self.symbol = symbol
            self.disclaimer = disclaimer
            self.update = update
            self.update_time = update_time
            self.server_time = server_time
            self.credit_count = credit_count
#OK
class r_technical_indicator():
    def __init__(self,status,code,msg,response,info):
        self.status = status
        self.code = code
        self.msg = msg
        self.response = response
        self.info = info

    class response():
        def __init__(self,oa_summary, count, indicators):
            self.oa_summary = oa_summary
            self.count = count
            self.indicators = indicators

    class count():
        def __init__(self,Total_Buy, Total_Sell, Total_Neutral, tiBuy, tiSell):
            self.Total_Buy = Total_Buy
            self.Total_Sell = Total_Sell
            self.Total_Neutral = Total_Neutral
            self.tiBuy = tiBuy
            self.tiSell = tiSell

    class indicators():
        def __init__(self, RSI14, STOCH9_6, STOCHRSI14, MACD12_26, WilliamsR, CCI14, ATR14, UltimateOscillator, summary):
            self.RSI14 = RSI14
            self.STOCH9_6 = STOCH9_6
            self.STOCHRSI14 = STOCHRSI14
            self.MACD12_26 = MACD12_26
            self.WilliamsR = WilliamsR
            self.CCI14 = CCI14
            self.ATR14 = ATR14
            self.UltimateOscillator = UltimateOscillator
            self.summary = summary

    class v_s():
        def __init__(self, v, s):
            self.v=v
            self.s=s

    class info:
        def __init__(self,id, decimal, symbol, period, disclaimer, update, update_time, server_time,credit_count):
            self.id = id
            self.decimal = decimal
            self.period = period
            self.symbol = symbol
            self.disclaimer = disclaimer
            self.update = update
            self.update_time = update_time
            self.server_time = server_time
            self.credit_count = credit_count