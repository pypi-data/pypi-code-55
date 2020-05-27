# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

registered = dict()


def register(name):
	def decorator(creator):
		registered[name] = creator
		return creator
	return decorator
