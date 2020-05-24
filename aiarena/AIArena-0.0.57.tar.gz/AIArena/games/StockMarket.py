import requests
import json


class StockMarket:
    """This implements a game of a Stock Market Simulator"""
    def __init__(self, state=None, players=None, APIKey=None, StockData=None):
        #Game Constants
        self.startValue = 10**6
        self.interval = 15
        self.APIKey = APIKey
        if APIKey is None and StockData is None:
            with open("SM_SampleData.txt") as f:
                StockData = json.load(f)

        if players is None:
            self.players = []
        else:
            self.players = players

        if state:
            self.state = state
            for p in self.players:
                if p.id not in self.state["portfolios"]:#new players
                    self.state["portfolios"][p.id] = {
                        "cash":self.startValue,
                        "stocks":{},
                        "trades":[]
                    }
        else:
            self.state = {
                "endDate": "endDate",
                "symbols": ["FB","AMZN","AAPL","NFLX","GOOGL"],
                "data":{},
                "players": players,
                "portfolios":{}
            }

            for s in self.state["symbols"]:
                self.state["data"][s] = []

            for p in self.players:
                self.state["portfolios"][p.id] = {
                    "cash":self.startValue,
                    "stocks":{},
                    "trades":[]
                }

        self.cached = {}
        if StockData is not None:
            for s, data in StockData.items():
                self.cached[s] = True
                self.state["data"][s] = data
                #get last
                #last = sorted(list(data),reverse=True)[0]
                #self.state["data"][s]["last"] = data[last]




    def print(self):
        print("---------------")
        for id, port in self.state["portfolios"].items():
            print(id)
            print(port['cash'])
            print(port['stocks'])
        print("---------------")

    def gatherStockData(self):
        for sym in self.state["symbols"]:
            if sym in self.cached:
                continue
            prices = self.getStockData(sym, str(self.interval)+"min")
            self.state["data"][sym] = prices + self.state["data"][sym]
            #print(self.state["data"][sym])

    def getStockData(self, symbol, interval):
        payload = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.APIKey
        }

        r = requests.get("https://www.alphavantage.co/query", payload)
        if r.status_code == 200:
            data = json.loads(r.content.decode())
            #last = data["Meta Data"]["3. Last Refreshed"]
            prices = []
            for date, d in data["Time Series (" + interval + ")"].items():
                prices.append(float(d['4. close']))
            return prices
        else:
            print("An error occured:", r.status_code, r.content)

    def validateMove(self, move):
        pass


    def validateTrade(self, trade, portfolio):
        if trade["symbol"] in self.state["symbols"]:
            if trade["action"] == "buy":
                cost = trade["quantity"] * self.state["data"][trade["symbol"]][0]
                if cost < portfolio['cash']:
                    return True
            elif trade["action"] == "sell":
                if trade["symbol"] in portfolio["stocks"] and trade["quantity"] <= portfolio["stocks"][trade["symbol"]]:
                    return True
        return False

    def makeTrade(self, trade, portfolio, aid):#Assumes trade was validated
        cost = trade["quantity"] * self.state["data"][trade["symbol"]][0]
        if trade["action"] == "buy":
            self.state['portfolios'][aid]['cash'] -= cost
            if trade["symbol"] in portfolio['stocks']:
                self.state['portfolios'][aid]['stocks'][trade["symbol"]] += trade["quantity"]
            else:
                self.state['portfolios'][aid]['stocks'][trade["symbol"]] = trade["quantity"]
        elif trade["action"] == "sell":
            self.state['portfolios'][aid]['cash'] += cost
            self.state['portfolios'][aid]['stocks'][trade["symbol"]] -= trade["quantity"]

    def makeMove(self, move):#assumes move has been validated
        for trade in move['trades']:
            portfolio = self.state['portfolios'][move['aid']]
            if self.validateTrade(trade, portfolio):
                self.makeTrade(trade,portfolio,move['aid'])
                self.state['portfolios'][move['aid']]['trades'].append(trade)

    def postMove(self):
        pass

    def endGame(self, winner):
        #print("Winner", winner)
        #print(self.state["players"][winner])
        self.state["Winner"] = winner

    def exportData(self):
        data = {}
        for s in self.state["symbols"]:
            data[s] = self.state["data"][s]
        return data

    def exportValue(self, id):
        val = self.state['portfolios'][id]['cash']
        for ticker, quant in self.state['portfolios'][id]['stocks'].items():
            val += quant * self.state["data"][ticker][0]
        return val

import AIArena


if __name__ == "__main__":
    class lilStockBuddy(AIArena.AI):  # <2>
        def __init__(self, name):
            super().__init__(name, "StockMarket")

    ai1 = lilStockBuddy("lilStockBuddy")
    sm = StockMarket(players=[ai1])
    sm.gatherStockData()
    print(json.dumps(sm.exportData()))

    trades = [
        {'action':"buy",'symbol':"FB",'quantity':100}
    ]

    move = {
        'aid': ai1.id,
        'trades': trades
    }

    sm.print()
    sm.makeMove(move)
    sm.print()

    trades = [
        {'action': "buy", 'symbol': "FB", 'quantity': 100}
    ]

    sm = StockMarket(players=[ai1], state=sm.state)

    move = {
        'aid': ai1.id,
        'trades': trades
    }

    sm.makeMove(move)
    sm.print()
    print(sm.exportValue(ai1.id))
