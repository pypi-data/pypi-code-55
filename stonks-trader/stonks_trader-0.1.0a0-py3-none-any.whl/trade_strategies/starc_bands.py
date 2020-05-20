from ta.volatility import AverageTrueRange
import matplotlib

from helpers import csv_utils, symbols_info
from helpers.plot import show_plot

matplotlib.use('TkAgg')


def find_starc_bands_signal(period=15, maperiod=5, multiplier=1.33) -> None:
    buy_signals = []
    for symbol_index in symbols_info.symbols_index:
            try:
                print(symbol_index)
                df = csv_utils.load_symbol(symbol_index)
                sma_value = df["<CLOSE>"].rolling(maperiod).mean()
                atr = AverageTrueRange(
                    close=df["<CLOSE>"], high=df["<HIGH>"], low=df["<LOW>"],
                    n=period
                ).average_true_range().values
                df["atr"] = atr
                df["sma"] = sma_value
                upper_bound = [i + j * multiplier for (i, j) in zip(sma_value, atr)]
                lower_bound = [i - j * multiplier for (i, j) in zip(sma_value, atr)]
                df["upper_bound"] = upper_bound
                df["lower_bound"] = lower_bound
                if df["<CLOSE>"].iloc[-1] < df["lower_bound"].iloc[-1]:
                    buy_signals.append(df)
            except:
                print("error")
                continue

    print("starc_bands", buy_signals)
    for buy_signal in buy_signals:
        show_plot(buy_signal, x="<DTYYYYMMDD>", y=['lower_bound', 'upper_bound', '<CLOSE>'])
