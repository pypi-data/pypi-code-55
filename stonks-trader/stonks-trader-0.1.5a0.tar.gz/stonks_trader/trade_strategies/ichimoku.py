import pandas as pd
from pandas_ta import rsi, ichimoku

from helpers import csv_utils, symbols_info
import numpy as np
from helpers.validations import symbol_record_is_valid


def ichimoku_signals():
    signals = []
    for symbol_index in symbols_info.symbols_index:
        df = csv_utils.load_symbol(symbol_index)
        if not symbol_record_is_valid(df):
            continue
        try:
            if ichimoku_test(df):
                signals.append(
                    symbol_index
                )
                print(
                    df["<TICKER>"].iloc[-1], df["<VOL>"].iloc[-1],
                    rsi(close=df.close, length=7).iloc[-1],
                    f'http://tsetmc.com/Loader.aspx?ParTree=151311&i={symbol_index}'
                )
        except ValueError as ex:
            continue


def check_ichimoku_signal(df: pd.DataFrame, symbol_index):
    try:
        high = df.high
        low = df.low
        close = df.close
        open = df.open
    except KeyError:
        return False
    ichimoku_df, _ = ichimoku(high, low, close)
    df = pd.concat([df, ichimoku_df], axis=1)
    df["rsi"] = rsi(close=close, length=10)

    df['above_cloud'] = 0
    df['above_cloud'] = np.where(
        (low > df["ISA_9"]) & (low > df["ISB_26"]), 1,
        df['above_cloud']
    )
    df['above_cloud'] = np.where(
        (high < df["ISA_9"]) & (high < df["ISB_26"]), -1,
        df['above_cloud']
    )

    df['A_above_B'] = np.where(
        (df['ISA_9'] > df['ISB_26']), 1, -1
    )

    df['tenkan_kiju_cross'] = np.NaN
    df['tenkan_kiju_cross'] = np.where(
        (df['ITS_9'].shift(1) <= df['IKS_26'].shift(1)) & (
                df['ITS_9'] > df['IKS_26']), 1, df['tenkan_kiju_cross'])
    df['tenkan_kiju_cross'] = np.where(
        (df['ITS_9'].shift(1) >= df['IKS_26'].shift(1)) & (
                df['ITS_9'] < df['IKS_26']), -1, df['tenkan_kiju_cross'])

    df['price_tenkan_cross'] = np.NaN
    df['price_tenkan_cross'] = np.where(
        (open.shift(1) <= df['ITS_9'].shift(1)) & (open > df['ITS_9']), 1,
        df['price_tenkan_cross'])
    df['price_tenkan_cross'] = np.where(
        (open.shift(1) >= df['ITS_9'].shift(1)) & (open < df['ITS_9']), -1,
        df['price_tenkan_cross'])

    df['buy'] = np.NaN
    df['buy'] = np.where(
        (df['above_cloud'].shift(1) == 1) & (df['A_above_B'].shift(1) == 1) &
        (
                (df['tenkan_kiju_cross'].shift(1) == 1) |
                (df['price_tenkan_cross'].shift(1) == 1)
        ),
        1,
        df['buy']
    )
    df['buy'] = np.where(df['tenkan_kiju_cross'].shift(1) == -1, 0, df['buy'])
    df['buy'].ffill(inplace=True)

    df['sell'] = np.NaN
    df['sell'] = np.where(
        (df['above_cloud'].shift(1) == -1) &
        (df['A_above_B'].shift(1) == -1) &
        (
                (df['tenkan_kiju_cross'].shift(1) == -1) |
                (df['price_tenkan_cross'].shift(1) == -1)
        ),
        -1,
        df['sell']
    )
    df['sell'] = np.where(df['tenkan_kiju_cross'].shift(1) == 1, 0, df['sell'])
    df['sell'].ffill(inplace=True)

    ichimku_cloud_cond = ichimoku_df["ISA_9"].iloc[-1] > \
                         ichimoku_df["ISB_26"].iloc[-1]
    conv_over_base = ichimoku_df['ITS_9'].iloc[-1] > \
                     ichimoku_df["IKS_26"].iloc[-1]
    price_over_cloud = (
            int(close.iloc[-1]) >= int(ichimoku_df["ISA_9"].iloc[-1]) and int(
        close.iloc[-1]) >= int(ichimoku_df["ISB_26"].iloc[-1])
    )
    rsi_cond = df["rsi"].iloc[-1] < 70

    # if ichimku_cloud_cond and conv_over_base and price_over_cloud and rsi_cond:
    #     return True

    if df["buy"].iloc[-1]:
        return True

    return False


def ichimoku_test(d):
    high = d.high
    low = d.low
    close = d.close
    open = d.open
    # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
    nine_period_high = high.rolling(window=9).max()
    nine_period_low = low.rolling(window=9).min()
    d['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

    # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
    period26_high = high.rolling(window=26).max()
    period26_low = low.rolling(window=26).min()
    d['kijun_sen'] = (period26_high + period26_low) / 2

    # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
    d['senkou_span_a'] = ((d['tenkan_sen'] + d['kijun_sen']) / 2).shift(26)

    # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
    period52_high = high.rolling(window=52).max()
    period52_low = low.rolling(window=52).min()
    d['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(52)

    # The most current closing price plotted 26 time periods behind (optional)
    d['chikou_span'] = close.shift(-26)

    d.dropna(inplace=True)

    d['above_cloud'] = 0
    d['above_cloud'] = np.where(
        (low > d['senkou_span_a']) & (low > d['senkou_span_b']), 1,
        d['above_cloud'])
    d['above_cloud'] = np.where(
        (high < d['senkou_span_a']) & (high < d['senkou_span_b']), -1,
        d['above_cloud'])

    d['A_above_B'] = np.where((d['senkou_span_a'] > d['senkou_span_b']), 1, -1)

    d['tenkan_kiju_cross'] = np.NaN
    d['tenkan_kiju_cross'] = np.where(
        (d['tenkan_sen'].shift(1) <= d['kijun_sen'].shift(1)) & (
                d['tenkan_sen'] > d['kijun_sen']), 1,
        d['tenkan_kiju_cross'])
    d['tenkan_kiju_cross'] = np.where(
        (d['tenkan_sen'].shift(1) >= d['kijun_sen'].shift(1)) & (
                d['tenkan_sen'] < d['kijun_sen']), -1,
        d['tenkan_kiju_cross'])

    d['price_tenkan_cross'] = np.NaN
    d['price_tenkan_cross'] = np.where(
        (open.shift(1) <= d['tenkan_sen'].shift(1)) & (open > d['tenkan_sen']),
        1, d['price_tenkan_cross'])
    d['price_tenkan_cross'] = np.where(
        (open.shift(1) >= d['tenkan_sen'].shift(1)) & (open < d['tenkan_sen']),
        -1, d['price_tenkan_cross'])

    d['buy'] = np.NaN
    d['buy'] = np.where(
        (d['above_cloud'].shift(1) == 1) & (d['A_above_B'].shift(1) == 1) & (
                (d['tenkan_kiju_cross'].shift(1) == 1) | (
                d['price_tenkan_cross'].shift(1) == 1)), 1, d['buy'])
    d['buy'] = np.where(d['tenkan_kiju_cross'].shift(1) == -1, 0, d['buy'])
    d['buy'].ffill(inplace=True)

    d['sell'] = np.NaN
    d['sell'] = np.where(
        (d['above_cloud'].shift(1) == -1) & (d['A_above_B'].shift(1) == -1) & (
                (d['tenkan_kiju_cross'].shift(1) == -1) | (
                d['price_tenkan_cross'].shift(1) == -1)), -1,
        d['sell'])
    d['sell'] = np.where(d['tenkan_kiju_cross'].shift(1) == 1, 0, d['sell'])
    d['sell'].ffill(inplace=True)

    for i in range(1, 3):
        if d['buy'].tail().iloc(i):
            return True

    return False
