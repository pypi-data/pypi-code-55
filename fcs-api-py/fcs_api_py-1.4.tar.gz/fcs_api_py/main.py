import requests
import json
from . import response_data_types as rdt

class Forex():
    def __init__(self, access_key):
        """Initializes with the access key.
        
            access_key string Access key generated in https://fcsapi.com/
        """
        self.access_key = access_key
    #OK
    def currency_latest_price(self, symbols):
        """Print a response with the latest price of a currency, or group of currency (comma separated).

            symbols string The symbol of the currency, example: "EUR/USD".

            returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    id
                    price
                    change
                    chg_per
                    last_change
                    symbol
                info
                    server_time
                    credit_count
        """
        self.symbols = symbols
        symbols = symbols.upper()
        url = "https://fcsapi.com/api-v2/forex/latest?symbol="+symbols+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_currency_latest_price.item_response(
                id = i["id"],
                price = i["price"],
                change = i["change"],
                chg_per = i["chg_per"],
                last_changed = i["last_changed"],
                symbol = i["symbol"]
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_currency_latest_price.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_currency_latest_price(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )
        return obj
    #OK
    def list_symbols(self):
        """List all supported symbols in the API.

            returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    id
                    decimal
                    symbol
                info
                    server_time
                    credit_count
        """
        url = "https://fcsapi.com/api-v2/forex/list?type=forex&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_list_symbols.item_response(
                id = i["id"],
                decimal = i["decimal"],
                symbol = i["symbol"]
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_list_symbols.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_list_symbols(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )
        return obj
    #OK
    def currency_details(self, symbols):
        """Get all the details about Forex currencies. Or group of currency (comma separated). Details like its name, country name.

            symbols string The symbol or gruop of symbols, example: "EUR".

            returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    short_name
                    name
                    country
                    code_n
                    subunit
                    website
                    symbol
                    bank
                    banknotes
                    coins
                    icon
                    type
                    symbol_2
                    banknotes_2
                    coins_2
                info
                    server_time
                    credit_count
        """
        self.symbols = symbols
        symbols = symbols.upper()
        url = "https://fcsapi.com/api-v2/forex/profile?symbol="+symbols+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_currency_details.item_response(
                short_name = i["short_name"],
                name = i["name"],
                country = i["country"],
                code_n = i["code_n"],
                subunit = i["subunit"],
                website = i["website"],
                symbol = i["symbol"],
                bank = i["bank"],
                banknotes = i["banknotes"],
                coins = i["coins"],
                icon = i["icon"],
                type = i["type"],
                symbol_2 = i["symbol_2"],
                banknotes_2 = i["banknotes_2"],
                coins_2 = i["coins_2"],
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_currency_details.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_currency_details(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )

        return obj
    #OK
    def currency_converter(self, origin_currency, dest_currency, amount):
        """Convert an amount from Origin to Destination currency.

            origin_currency string The Symbol of the original amount. Example: USD.

            dest_currency string The Symbol of the converted amount. Example: ARS.

            amount int The amount to convert.

            returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    price_1x_origin
                    price_1x_dest
                    total
                info
                    server_time
                    credit_count
        """
        self.origin_currency = origin_currency
        self.dest_currency = dest_currency
        self.amount = amount
        origin_currency = origin_currency.upper()
        dest_currency = dest_currency.upper()
        url = "https://fcsapi.com/api-v2/forex/converter?pair1="+origin_currency+"&pair2="+dest_currency+"&amount="+str(amount)+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        item_r = rdt.r_currency_converter.item_response(
            price_1x_origin = res["response"]["price_1x_"+origin_currency],
            price_1x_dest = res["response"]["price_1x_"+dest_currency],
            total = res["response"]["total"]
        )
        list_r.append(item_r)
        #Load info object
        info = rdt.r_currency_converter.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_currency_converter(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )

        return obj
    #OK
    def base_currency(self, symbol, type="forex"):
        """
        On the base of 1 currency, it will return all quote prices of all available currencies.

        symbol string The symbol of the currency.

        type string the type of the response, it can be 'forex' or 'crypto'. Default value: 'forex'.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    key (currency) : value (value)
                info
                    base
                    type
                    server_time
                    credit_count
        """
        self.symbol = symbol
        symbol = symbol.upper()
        url = "https://fcsapi.com/api-v2/forex/base_latest?symbol="+symbol+"&type="+type+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the dict manually
        dict_r = {}
        dict_r = res["response"]
        #Load info object
        info = rdt.r_base_currency.info(
                base=res["info"]["base"],
                type=res["info"]["type"],
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_base_currency(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=dict_r,
            info=info
        )

        return obj
    #OK
    def currency_cross(self, symbol):
        """
        Return all related currencies of required currency.

        symbol string The currency to return.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    id
                    price
                    change
                    chg_per
                    last_changed
                    type
                    symbol
                info
                    server_time
                    credit_count
        """
        self.symbol = symbol
        symbol = symbol.upper()
        url = "https://fcsapi.com/api-v2/forex/cross?symbol="+symbol+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_currency_cross.item_response(
                id = i["id"],
                price = i["price"],
                change = i["change"],
                chg_per = i["chg_per"],
                last_changed = i["last_changed"],
                type = i["type"],
                symbol = i["symbol"]
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_currency_cross.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_currency_cross(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )

        return obj
    #OK
    def last_candle(self, symbols, period):
        """
        Return the last candle price of a currency (Open,High,Low,Close).

        symbol string The currency or group of currencies to return.

        period string The period of the data to retrieve, it can be: 1m, 5m, 15m, 30m,1h, 5h, 1d, 1w, month.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    o
                    h
                    l
                    c
                    t
                    tm
                    symbol
                info
                    server_time
                    credit_count
        """
        self.symbols = symbols
        self.period = period
        symbols = symbols.lower()
        url = "https://fcsapi.com/api-v2/forex/candle?symbol="+symbols+"&period="+period+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_last_candle.item_response(
                o = i["o"],
                h = i["h"],
                l = i["l"],
                c = i["c"],
                t = i["t"],
                tm = i["tm"],
                symbol = i["symbol"]
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_last_candle.info(
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_last_candle(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )

        return obj
    #OK
    def historical_price(self, symbol, period, from_date, to_date):
        """
        Return the historical exchange price data for all supported symbols.

        symbol string The currency or group of currencies to return.

        period string The period of the data to retrieve, it can be: 1m, 5m, 15m, 30m,1h, 5h, 1d, 1w, month.

        from_date string The date from. Format: YYYY-MM-DDThh:mm. Ex(2020-05-08T12:00)

        to_date string The date to. Format: YYYY-MM-DDThh:mm. Ex(2020-05-08T12:00)

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    o
                    h
                    l
                    c
                    t
                    tm
                info
                    id
                    decimal
                    symbol
                    period
                    server_time
                    credit_count
        """
        self.symbol = symbol
        self.period = period
        self.from_date = from_date
        self.to_date = to_date
        symbol = symbol.upper()
        period = period.lower()
        from_date = from_date.upper()
        to_date = to_date.upper()

        url = "https://fcsapi.com/api-v2/forex/history?symbol="+symbol+"&period="+period+"&from="+from_date+"&to="+to_date+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the list manually
        list_r = []
        for i in res["response"]:
            item_r = rdt.r_historical_price.item_response(
                o = i["o"],
                h = i["h"],
                l = i["l"],
                c = i["c"],
                t = i["t"],
                tm = i["tm"],
            )
            list_r.append(item_r)
        #Load info object
        info = rdt.r_historical_price.info(
                id = res["info"]["id"],
                decimal = res["info"]["decimal"],
                symbol = res["info"]["symbol"],
                period = res["info"]["period"],
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_historical_price(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=list_r,
            info=info
        )

        return obj
    #OK
    def pivot_points(self, symbol, period):
        """
        Return market indicators for all supported symbols.

        symbol string The currency to return.

        period string The period of the data to retrieve, it can be: 1m, 5m, 15m, 30m,1h, 5h, 1d, 1w, month.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    oa_summary
                    pivot_point
                        classic
                            pp
                            R1
                            R2
                            R3
                            S1
                            S2
                            S3
                        fibonacci
                            pp
                            R1
                            R2
                            R3
                            S1
                            S2
                            S3
                        camarilla
                            pp
                            R1
                            R2
                            R3
                            R4
                            S1
                            S2
                            S3
                            S4
                        woodie
                            pp
                            R1
                            R2
                            S1
                            S2
                        demark
                            high
                            low
                            R1
                            S1
                info
                    id
                    decimal
                    symbol
                    period
                    disclaimer
                    update
                    update_time
                    server_time
                    credit_count
        """
        self.period = period
        self.symbol = symbol
        symbol = symbol.upper()
        period = period.lower()
        url = "https://fcsapi.com/api-v2/forex/pivot_points?symbol="+symbol+"&period="+period+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the dict manually
        classic = rdt.r_pivot_points.classic(
            pp = res["response"]["pivot_point"]["classic"]["pp"],
            R1 = res["response"]["pivot_point"]["classic"]["R1"],
            R2 = res["response"]["pivot_point"]["classic"]["R2"],
            R3 = res["response"]["pivot_point"]["classic"]["R3"],
            S1 = res["response"]["pivot_point"]["classic"]["S1"],
            S2 = res["response"]["pivot_point"]["classic"]["S2"],
            S3 = res["response"]["pivot_point"]["classic"]["S3"]
        )

        fibonacci = rdt.r_pivot_points.fibonacci(
            pp = res["response"]["pivot_point"]["fibonacci"]["pp"],
            R1 = res["response"]["pivot_point"]["fibonacci"]["R1"],
            R2 = res["response"]["pivot_point"]["fibonacci"]["R2"],
            R3 = res["response"]["pivot_point"]["fibonacci"]["R3"],
            S1 = res["response"]["pivot_point"]["fibonacci"]["S1"],
            S2 = res["response"]["pivot_point"]["fibonacci"]["S2"],
            S3 = res["response"]["pivot_point"]["fibonacci"]["S3"]
        )

        camarilla = rdt.r_pivot_points.camarilla(
            pp = res["response"]["pivot_point"]["camarilla"]["pp"],
            R1 = res["response"]["pivot_point"]["camarilla"]["R1"],
            R2 = res["response"]["pivot_point"]["camarilla"]["R2"],
            R3 = res["response"]["pivot_point"]["camarilla"]["R3"],
            R4 = res["response"]["pivot_point"]["camarilla"]["R4"],
            S1 = res["response"]["pivot_point"]["camarilla"]["S1"],
            S2 = res["response"]["pivot_point"]["camarilla"]["S2"],
            S3 = res["response"]["pivot_point"]["camarilla"]["S3"],
            S4 = res["response"]["pivot_point"]["camarilla"]["S4"]
        )

        woodie = rdt.r_pivot_points.woodie(
            pp = res["response"]["pivot_point"]["woodie"]["pp"],
            R1 = res["response"]["pivot_point"]["woodie"]["R1"],
            R2 = res["response"]["pivot_point"]["woodie"]["R2"],
            S1 = res["response"]["pivot_point"]["woodie"]["S1"],
            S2 = res["response"]["pivot_point"]["woodie"]["S2"],
        )

        demark = rdt.r_pivot_points.demark(
            high = res["response"]["pivot_point"]["demark"]["high"],
            low = res["response"]["pivot_point"]["demark"]["low"],
            R1 = res["response"]["pivot_point"]["demark"]["R1"],
            S1 = res["response"]["pivot_point"]["demark"]["S1"],
        )

        pivot_point = rdt.r_pivot_points.pivot_point(
            classic = classic,
            fibonacci = fibonacci, 
            camarilla = camarilla, 
            woodie = woodie, 
            demark = demark
        )
        response = rdt.r_pivot_points.response(
            oa_summary = res["response"]["oa_summary"],
            pivot_point = pivot_point
        )
        #Load info object
        info = rdt.r_pivot_points.info(
                id=res["info"]["id"],
                decimal = res["info"]["decimal"],
                symbol = res["info"]["symbol"],
                period = res["info"]["period"],
                disclaimer = res["info"]["disclaimer"],
                update=res["info"]["update"],
                update_time=res["info"]["update_time"],
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_pivot_points(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=response,
            info=info
        )

        return obj
    #OK
    def moving_average(self, symbol, period):
        """
        Return moving average for all supported symbols.

        symbol string The currency to return.

        period string The period of the data to retrieve, it can be: 1m, 5m, 15m, 30m,1h, 5h, 1d, 1w, month.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    oa_summary
                    count
                        TotalBuy
                        Total_Sell
                        Total_Neutral
                        maBuy
                        maSell
                    ma_avg
                        SMA
                            MA5
                                v
                                s
                            MA10
                                v
                                s
                            MA20
                                v
                                s
                            MA50
                                v
                                s
                            MA100
                                v
                                s
                            MA200
                                v
                                s
                        EMA
                            MA5
                                v
                                s
                            MA10
                                v
                                s
                            MA20
                                v
                                s
                            MA50
                                v
                                s
                            MA100
                                v
                                s
                            MA200
                                v
                                s
                        summary
                info
                    id
                    decimal
                    symbol
                    period
                    disclaimer
                    update
                    update_time
                    server_time
                    credit_count
        """
        self.period = period
        self.symbol = symbol
        symbol = symbol.upper()
        period = period.lower()
        url = "https://fcsapi.com/api-v2/forex/ma_avg?symbol="+symbol+"&period="+period+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the dict manually
        MA5=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA5"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA5"]["s"])
        MA10=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA10"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA10"]["s"])
        MA20=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA20"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA20"]["s"])
        MA50=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA50"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA50"]["s"])
        MA100=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA100"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA100"]["s"])
        MA200=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["EMA"]["MA200"]["v"],
            s=res["response"]["ma_avg"]["EMA"]["MA200"]["s"])

        EMA = rdt.r_moving_average.EMA(
            MA5= MA5,
            MA10= MA10,
            MA20= MA20,
            MA50= MA50,
            MA100= MA100,
            MA200= MA200,
        )

        MA5=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA5"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA5"]["s"])
        MA10=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA10"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA10"]["s"])
        MA20=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA20"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA20"]["s"])
        MA50=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA50"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA50"]["s"])
        MA100=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA100"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA100"]["s"])
        MA200=rdt.r_moving_average.v_s(
            v=res["response"]["ma_avg"]["SMA"]["MA200"]["v"],
            s=res["response"]["ma_avg"]["SMA"]["MA200"]["s"])

        SMA = rdt.r_moving_average.SMA(
            MA5= MA5,
            MA10= MA10,
            MA20= MA20,
            MA50= MA50,
            MA100= MA100,
            MA200= MA200,
        )

        ma_avg = rdt.r_moving_average.ma_avg(
            SMA=SMA,
            EMA=EMA,
            summary=res["response"]["ma_avg"]["summary"]
        )

        count = rdt.r_moving_average.count(
            Total_Buy = res["response"]["count"]["Total_Buy"],
            Total_Sell = res["response"]["count"]["Total_Sell"], 
            Total_Neutral = res["response"]["count"]["Total_Neutral"], 
            maBuy = res["response"]["count"]["maBuy"], 
            maSell = res["response"]["count"]["maSell"]
        )
        response = rdt.r_moving_average.response(
            oa_summary = res["response"]["oa_summary"],
            count = count,
            ma_avg = ma_avg
        )
        #Load info object
        info = rdt.r_moving_average.info(
                id=res["info"]["id"],
                decimal = res["info"]["decimal"],
                symbol = res["info"]["symbol"],
                period = res["info"]["period"],
                disclaimer = res["info"]["disclaimer"],
                update=res["info"]["update"],
                update_time=res["info"]["update_time"],
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_moving_average(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=response,
            info=info
        )

        return obj
    #OK
    def technical_indicator(self, symbol, period):
        """
        Return technicals indicators for all supported symbols.

        symbol string The currency to return.

        period string The period of the data to retrieve, it can be: 1m, 5m, 15m, 30m,1h, 5h, 1d, 1w, month.

        returns A object with the following structure (Use dot(.) to access his childs):

            object
                status
                code
                msg
                response
                    oa_summary
                    count
                        TotalBuy
                        Total_Sell
                        Total_Neutral
                        tiBuy
                        tiSell
                    indicators
                        RSI14
                            v
                            s
                        STOCH9_6
                            v
                            s
                        STOCHRSI14
                            v
                            s
                        MACD12_26
                            v
                            s
                        WilliamsR
                            v
                            s
                        CCI14
                            v
                            s
                        ATR14
                            v
                            s
                        UltimateOscillator
                            v
                            s
                        summary
                info
                    id
                    decimal
                    symbol
                    period
                    disclaimer
                    update
                    update_time
                    server_time
                    credit_count
        """
        self.symbol = symbol
        self.period = period
        symbol.upper()
        period.lower()
        url = "https://fcsapi.com/api-v2/forex/indicators?symbol="+symbol+"&period="+period+"&access_key="+self.access_key
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload)
        res = json.loads(response.text.encode('utf8'))
        #Load the dict manually
        RSI14=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["RSI14"]["v"],
            s=res["response"]["indicators"]["RSI14"]["s"])
        STOCH9_6=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["STOCH9_6"]["v"],
            s=res["response"]["indicators"]["STOCH9_6"]["s"])
        STOCHRSI14=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["STOCHRSI14"]["v"],
            s=res["response"]["indicators"]["STOCHRSI14"]["s"])
        MACD12_26=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["MACD12_26"]["v"],
            s=res["response"]["indicators"]["MACD12_26"]["s"])
        WilliamsR=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["WilliamsR"]["v"],
            s=res["response"]["indicators"]["WilliamsR"]["s"])
        CCI14=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["CCI14"]["v"],
            s=res["response"]["indicators"]["CCI14"]["s"])
        ATR14=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["ATR14"]["v"],
            s=res["response"]["indicators"]["ATR14"]["s"])
        UltimateOscillator=rdt.r_technical_indicator.v_s(
            v=res["response"]["indicators"]["UltimateOscillator"]["v"],
            s=res["response"]["indicators"]["UltimateOscillator"]["s"])

        indicators = rdt.r_technical_indicator.indicators(
            UltimateOscillator=UltimateOscillator,
            ATR14=ATR14,
            CCI14=CCI14,
            WilliamsR=WilliamsR,
            MACD12_26=MACD12_26,
            STOCHRSI14=STOCHRSI14,
            STOCH9_6=STOCH9_6,
            RSI14=RSI14,
            summary=res["response"]["indicators"]["summary"]
        )

        count = rdt.r_technical_indicator.count(
            Total_Buy = res["response"]["count"]["Total_Buy"],
            Total_Sell = res["response"]["count"]["Total_Sell"], 
            Total_Neutral = res["response"]["count"]["Total_Neutral"], 
            tiBuy = res["response"]["count"]["tiBuy"], 
            tiSell = res["response"]["count"]["tiSell"]
        )
        response = rdt.r_technical_indicator.response(
            oa_summary = res["response"]["oa_summary"],
            count = count,
            indicators = indicators
        )
        #Load info object
        info = rdt.r_technical_indicator.info(
                id=res["info"]["id"],
                decimal = res["info"]["decimal"],
                symbol = res["info"]["symbol"],
                period = res["info"]["period"],
                disclaimer = res["info"]["disclaimer"],
                update=res["info"]["update"],
                update_time=res["info"]["update_time"],
                server_time=res["info"]["server_time"],
                credit_count=res["info"]["credit_count"]
            )
        #Load the main object
        obj = rdt.r_technical_indicator(
            status=res["status"],
            code=res["code"],
            msg=res["msg"],
            response=response,
            info=info
        )

        return obj