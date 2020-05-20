# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.3.0'

import typing as tp
from pathlib import Path
from kedro.context import load_context
from kedro.pipeline import Pipeline
from take_forecast.pipelines import preprocess, tune


def create_pipelines(**_) -> tp.Dict[str, Pipeline]:
	"""Create pipelines for project and users."""
	
	pipelines = dict()
	
	context = load_context(Path.cwd())
	loader = context.config_loader
	cases = loader.get('cases.yml')['cases']
	for case in cases:
		pl_preprocess = preprocess.create_pipeline(case=case)
		pl_tune = tune.create_pipeline(case=case)
		pipelines['{case}_preprocess'.format(case=case)] = pl_preprocess
		pipelines['{case}_tune'.format(case=case)] = pl_tune
	
	case = cases[0]
	pipelines['__default__'] =\
		pipelines['{case}_preprocess'.format(case=case)] +\
		pipelines['{case}_tune'.format(case=case)]
	
	return pipelines
