from .general import *
from .linearregression import *



# split timeseries into trend, season * trend and residual
def decompose(series, period):

    if (len(series) < 10):
        raise Exception('data is too small, must be at least 10 values')

    x = list(range(len(series)))
    lr = linear_regression(x, series)

    trend = f_x(x, lambda x: x * lr[0] + lr[1])
    detrend = series_diff(series, trend)
    seasonal = (seasonal_pattern(detrend, period) * (((len(detrend) + 1) // (period - 1)) + 1))[0:len(series)]
    residual = series_diff(detrend,seasonal, 0)
    
    return decomposed_seasonal_data(series, trend, detrend, seasonal, residual)

# unweighted rolling average
def moving_average(series, window):
    import math
    roller = []
    for i in range(math.floor(window / 2) + 1):
        roller.append(math.nan)
    for i in range(len(series) - window + 1):
        roller.append (mean(series[i:i+window]))
    for i in range(math.ceil(window / 2)):
        roller.append(math.nan)
    return roller[1:len(series) + 1]

# fourier transform to identify frequencies
def series_frequencies(series):
    import numpy as np
    # to remove the DC (usually a 0 peak) subtract the mean of the set from each value
    readings= []
    series_mean = mean(series)
    for i in series:
        readings.append(i - series_mean)
    fourierTransform = np.fft.rfft(readings)
    return fourierTransform

# fourier transform to identify frequencies
def cycle_periods(series):
    fourierTransform = series_frequencies(series)
    fourierTransform = fourierTransform[0:len(fourierTransform) // 2]
    signal_mean = mean(abs(fourierTransform))
    sigma = standard_deviation(abs(fourierTransform))
    for s in range(10,0,-1):
        peaks = matches(abs(fourierTransform), lambda t: t > signal_mean + (s * sigma))
        if 1 in peaks:
            peaks.remove(1)
        if len(peaks) > 0:
            for p in range(len(peaks)):
                peaks[p] = round(len(series) / peaks[p])
            return list(set(peaks))
    raise TypeError('No cycle identified')
    
# identify cyclic pattern of series data for period
def seasonal_pattern(series, period):
    pattern = []
    cycle_sum = [0] * period
    cycle_count = [0] * period
    for i in range(len(series)):
        cycle_sum[i % period] = cycle_sum[i % period] + series[i]
        cycle_count[i % period] = cycle_count[i % period] + 1
    for i in range(period):
        cycle_mean = cycle_sum[i] / cycle_count[i]
        pattern.append(cycle_mean)
    return pattern

# apply the seasonal patterns to the trend data
def product_series(series, cycles, trend):
    if not isinstance(cycles, list): 
        cycles = [cycles]
    base = trend.copy()
    for cycle in cycles:
        pattern = seasonal_pattern(series,cycle)
        for i in range(len(series)):
            base[i] = base[i] / pattern[i % cycle]
    return base

class decomposed_seasonal_data:

    def __init__(self, source, trend, detrend, seasonal, residual):
        self.source = source
        self.trend = trend
        self.detrend = detrend
        self.seasonal = seasonal
        self.residual = residual
        self.record = len(self.source)

    def plot(self):
        from matplotlib import pyplot as plt
        LARGE_FONT = 15
        plt.rc('font', size=LARGE_FONT)
        plt.figure(figsize=(20, 12))
        ax = plt.subplot(111)

        # source
        ax = plt.subplot(511)
        plt.ylabel('Source')
        ax.axhline(y=mean(self.source), color='#AAAAAA', linestyle=':')
        plt.plot(self.source, color='#6666CC')

        # regression
        ax = plt.subplot(512)
        plt.ylabel('Regression')
        ax.axhline(y=mean(self.trend), color='#AAAAAA', linestyle=':')
        plt.plot(self.trend, color='#6666CC')

        # seasonal pattern
        ax = plt.subplot(513)
        plt.ylabel('Seasonal')
        ax.axhline(y=mean(self.seasonal), color='#AAAAAA', linestyle=':')
        plt.plot(self.seasonal, color='#6666CC')
        
        # detrend
        ax = plt.subplot(514)
        plt.ylabel('Detrend')
        ax.axhline(y=mean(self.detrend), color='#AAAAAA', linestyle=':')
        plt.plot(self.detrend, color='#6666CC')

        # residual 
        ax = plt.subplot(515)
        plt.ylabel('Residual')
        ax.axhline(y=mean(self.residual), color='#AAAAAA', linestyle=':')
        plt.plot(self.residual, color='#6666CC')

        from matplotlib import pyplot as plt