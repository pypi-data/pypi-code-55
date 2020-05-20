import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial

from helpers.csv_utils import load_symbol
from helpers import symbols_info
from helpers.validations import symbol_record_is_valid
from helpers.plot import show_plot, with_subplot
import seaborn as sns


def find_trend():
    for symbol_index in symbols_info.test_symbol:
        df = load_symbol(symbol_index)
        if not symbol_record_is_valid(df):
            continue
        check_stochastic_signal(df)


def check_stochastic_signal(df: pd.DataFrame):
    df = df.tail(60)
    import matplotlib.pyplot as plt
    # sns.regplot(x=[i for i in range(len(df.date))], y=df.close, data=df, fit_reg=True)
    coefs = np.polyfit(df.close, [i for i in range(len(df.date))], 1)
    f = np.poly1d(coefs)
    ffit = Polynomial(coefs)
    df["trend"] = f(df.close)
    df.plot(x="date", y=["close", "trend"])
    # plt.plot(df.close, )
    plt.show()
    return df
