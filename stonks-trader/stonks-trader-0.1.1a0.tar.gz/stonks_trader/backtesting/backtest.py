import pandas as pd

from stonks_trader.trade_strategies import trade_strategies


def backtest(df: pd.DataFrame, strategy):
    strategy = trade_strategies[strategy](
        df=df,
    )
    strategy.analyze()
    df = strategy.df
    strategy.dump(n=100, path="jem.csv")
    buy_prices = []
    sell_prices = []
    profit = []
    for i in df.index:
        if df.loc[i, "buy_signal"]:
            close = df.loc[i, "close"]
            print("buy on ", df.loc[i, "date"], close)
            buy_prices.append(close)
        if df.loc[i, "sell_signal"] and len(buy_prices) > len(sell_prices):
            close = df.loc[i, "close"]
            print("sell on ", df.loc[i, "date"], close)
            buy_avg = sum(buy_prices) / len(buy_prices)
            print(buy_avg, close)
            profit.append(
                (close - buy_avg) / ((buy_avg + close) / 2) * 100
            )
            print(profit[-1])
            buy_prices = []
    print(profit)
    print("total profit", sum(profit))
    # strategy.plot(name="", n=100)
