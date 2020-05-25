# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.6.1'

import itertools as it
import typing as tp
import warnings as wn
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	import statsmodels.api as sm

KW = tp.Dict[str, tp.Any]
HP = tp.Dict[str, int]
MHP = tp.Dict[str, KW]
TS = pd.Series
DF = pd.DataFrame
HP_HP = tp.Tuple[HP, HP]
DF_HP = tp.Tuple[DF, HP]
DF_DF = tp.Tuple[DF, DF]
DF_DF_HP = tp.Tuple[DF, DF, HP]


def seasonality_test(ts: TS, threshold: float, s_start: int, s_stop: int) -> tp.Tuple[bool, float, int]:
	s_stop = min(s_stop, ts.shape[0] // 4)
	is_seasonal = False
	s_range = list(range(s_start, s_stop))
	qstats = list()
	n = len(ts)
	
	cyclical = sm.tsa.filters.hpfilter(ts)[0]
	acf = sm.tsa.acf(cyclical, alpha=None, nlags=2 * s_stop, fft=False)
	for s in s_range:
		qstats.append(n * (n + 2) * sum([np.square(np.max([0, acf[k * s]])) / (n - k * s) for k in range(1, 3)]))
		if qstats[-1] > threshold:
			is_seasonal = True
	return is_seasonal, np.max(qstats), s_range[int(np.argmax(qstats))]


def stationarity_test(ts: TS, threshold: float, n_diff: int) -> tp.Tuple[int, TS]:
	d = 0
	ts = ts.dropna()
	ts_stationary = ts
	
	for k in range(n_diff):
		adf, *_ = sm.tsa.adfuller(ts[k:])
		ts = ts.diff()
		if adf > threshold:
			d += 1
			ts_stationary = ts
	return d, ts_stationary


def autocorrelation_test(ts: TS, s: int) -> tp.Tuple[int, int]:
	nlags = (s - 1) if s else min(15, ts.shape[0] // 2)
	ts = ts.dropna()
	acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
	pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
	
	acf_nnull = acf_confint.prod(axis=1) > 0
	pacf_nnull = pacf_confint.prod(axis=1) > 0
	q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
	p_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
	
	return p_max, q_max


def seasonal_autocorrelation_test(ts: TS, s: int, n_cycles: int) -> tp.Tuple[int, int]:
	if s == 0:
		return 0, 0
	
	n_cycles = min(n_cycles, int(0.5 * ts.shape[0] / s))
	nlags = s * n_cycles
	acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
	pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
	
	acf = acf[::s]
	acf_confint = acf_confint[::s]
	pacf = pacf[::s]
	pacf_confint = pacf_confint[::s]
	
	acf_nnull = acf_confint.prod(axis=1) > 0
	pacf_nnull = pacf_confint.prod(axis=1) > 0
	acf_nnull[np.abs(acf) > 1] = False
	pacf_nnull[np.abs(pacf) > 1] = False
	Q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
	P_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
	
	return P_max, Q_max


def model_selection(ts: TS, pdq: tp.Tuple[int, int, int], sPQ: tp.Optional[tp.Tuple[int, int, int]]=None) -> KW:
	if sPQ:
		ranges = [range(lim + 1) for lim in (pdq[0], pdq[1], pdq[2], sPQ[1], sPQ[2])]
		to_kwargs = (lambda params: {
			'order': (params[0], params[1], params[2]),
			'seasonal_order': (params[3], (pdq[1] - params[1]), params[4], sPQ[0])
		})
	else:
		ranges = [range(lim + 1) for lim in (pdq[0], pdq[2])]
		to_kwargs = (lambda params: {
			'order': (params[0], pdq[1], params[1])
		})
	
	min_aic = dict()
	for params in it.product(*ranges):
		kwargs = to_kwargs(params)
		try:
			with wn.catch_warnings():
				wn.simplefilter('ignore')
				result = sm.tsa.SARIMAX(ts, **kwargs).fit(disp=False)
		except:
			continue
		else:
			if result.aic < min_aic.get('aic', result.aic + 1):
				min_aic = {
					'aic': result.aic,
					'kwargs': kwargs
				}
	
	return min_aic['kwargs']


def decompose_seasonal(df: DF, threshold: float, s_start: int, s_stop: int) -> DF_DF_HP:
	dct_s = dict()
	df_seasonal = pd.DataFrame(columns=df.columns)
	df_not_seasonal = pd.DataFrame(columns=df.columns)
	for name, ts in df.items():
		is_seasonal, qstats, s = seasonality_test(ts, threshold, s_start, s_stop)
		if is_seasonal:
			dct_s[name] = s
			result = sm.tsa.STL(df[name], period=s).fit()
			df_seasonal[name] = result.seasonal
			df_not_seasonal[name] = result.trend + result.resid
		else:
			dct_s[name] = 0
			df_not_seasonal[name] = ts
	return df_seasonal, df_not_seasonal, dct_s


def transform_to_stationary(df: DF, threshold: float, n_diff: int) -> DF_HP:
	dct_d = dict()
	df_stationary = pd.DataFrame(columns=df.columns)
	for name, ts in df.items():
		d, ts_stationary = stationarity_test(ts, threshold, n_diff)
		dct_d[name] = d
		df_stationary[name] = ts_stationary
	return df_stationary, dct_d


def analyse_autocorrelation(df: DF, dct_s: HP) -> HP_HP:
	dct_p_max = dict()
	dct_q_max = dict()
	for name, ts in df.items():
		p_max, q_max = autocorrelation_test(ts, dct_s[name])
		dct_p_max[name] = p_max
		dct_q_max[name] = q_max
	return dct_p_max, dct_q_max


def analyse_seasonal_autocorrelation(df: DF, dct_s: HP, n_cycles: int) -> HP_HP:
	dct_P_max = dict()
	dct_Q_max = dict()
	for name, ts in df.items():
		P_max, Q_max = seasonal_autocorrelation_test(ts, dct_s[name], n_cycles)
		dct_P_max[name] = P_max
		dct_Q_max[name] = Q_max
	return dct_P_max, dct_Q_max


def split_train_test(df: DF, r_split: int) -> DF_DF:
	k = int(r_split * len(df))
	df_train = df.iloc[:k]
	df_test = df.iloc[k:]
	return df_train, df_test


def tune_sarima(df: DF, dct_s: HP, dct_d: HP, dct_p_max: HP, dct_q_max: HP, dct_P_max: HP, dct_Q_max: HP) -> MHP:
	dct_kwargs = dict()
	for name, ts in df.items():
		p = dct_p_max[name]
		d = dct_d[name]
		q = dct_q_max[name]
		s = dct_s[name]
		P = dct_P_max[name]
		Q = dct_Q_max[name]
		pdq = (p, d, q)
		sPQ = (s, P, Q) if s else None
		kwargs = model_selection(ts, pdq, sPQ)
		dct_kwargs[name] = kwargs
	return dct_kwargs
