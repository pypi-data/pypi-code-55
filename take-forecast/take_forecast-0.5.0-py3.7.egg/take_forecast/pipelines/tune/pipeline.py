# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.5.0'

from kedro.pipeline import Pipeline, node
from .nodes import decompose_seasonal
from .nodes import transform_to_stationary
from .nodes import analyse_autocorrelation
from .nodes import analyse_seasonal_autocorrelation
from .nodes import split_train_test
from .nodes import tune_sarima


def create_pipeline(**kwargs):
	case = kwargs['case']
	c = (lambda name: '{case}_{name}'.format(case=case, name=name))
	p = (lambda name: 'params:{case}_{name}'.format(case=case, name=name))
	return Pipeline(
		[
			node(
				decompose_seasonal,
				[c('new_users'), p('seasonal_threshold'), p('s_start'), p('s_stop')],
				[c('seasonal'), c('not_seasonal'), c('s')],
				name='decompose_seasonal'
			),
			node(
				transform_to_stationary,
				[c('new_users'), p('adf_threshold'), p('adf_n_diff')],
				[c('stationary'), c('d')],
				name='transform_to_stationary'
			),
			node(
				analyse_autocorrelation,
				[c('stationary'), c('s')],
				[c('p_max'), c('q_max')],
				name='analyse_autocorrelation'
			),
			node(
				analyse_seasonal_autocorrelation,
				[c('new_users'), c('s'), p('seasonal_acf_n_cycles')],
				[c('sP_max'), c('sQ_max')],
				name='analyse_seasonal_autocorrelation'
			),
			node(
				split_train_test,
				[c('new_users'), p('r_split')],
				[c('train'), c('test')],
				name='split_train_test'
			),
			node(
				tune_sarima,
				[c('train'), c('s'), c('d'), c('p_max'), c('q_max'), c('sP_max'), c('sQ_max')],
				c('hyper_parameters'),
				name='tune_sarima'
			)
		]
	)
