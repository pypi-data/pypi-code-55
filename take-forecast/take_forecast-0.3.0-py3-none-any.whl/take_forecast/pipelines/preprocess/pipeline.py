# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

from .pipelines import registered


def create_pipeline(**kwargs):
	case = kwargs['case']
	creator = registered[case]
	return creator()
