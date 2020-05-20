import pandas as pd
from ta.trend import macd_signal, macd, macd_diff

from helpers.csv_utils import load_symbol
from helpers.plot import show_plot
from config import DAILY_RECORD_FIELDS
from trade_strategies.stochastic import check_stochastic_signal
from trade_strategies.rsi import check_rsi_signal
from helpers.validations import symbol_record_is_valid


def find_macd_stock_rsi_signals():
    for symbol_index in ["38547060135156069"]:
        df = load_symbol(symbol_index)
        if not symbol_record_is_valid(df):
            continue
        check_macd_stoch_rsi(df)
        try:
            show_plot(df, y=["rsi", "stoch_k", "stoch_d"])
            # for i in range(1, 5):
            #     if df["buy_signal"].tail().iloc[i]:
            #         print(df.tail())
            #         print(
            #             f'http://tsetmc.com/Loader.aspx?ParTree=151311&i={symbol_index}')
            #         show_plot(df, y=["macd_diff", "macd", "macd_signal"])
        except:
            continue


def check_macd_stoch_rsi(df: pd.DataFrame):
    check_stochastic_signal(df)
    check_rsi_signal(df, rsi_below=30)
    df["macd_signal"] = macd_signal(df[DAILY_RECORD_FIELDS.close])
    df["macd"] = macd(df[DAILY_RECORD_FIELDS.close])
    df["macd_diff"] = macd_diff(df[DAILY_RECORD_FIELDS.close])
    yesterday_macd = df['macd'].shift(1)
    yesterday_macd_signal = df['macd_signal'].shift(1)
    df["macd_crossing_signal"] = (
            (df['macd_signal'] <= df['macd']) &
            (yesterday_macd_signal >= yesterday_macd)
            # (df["macd"] < 55)
    )
    df["buy_signal"] = (
            (df["stoch_buy_signal"]) &
            (df["rsi_buy_signal"])
            # df["macd_crossing_signal"]
    )


find_macd_stock_rsi_signals()
