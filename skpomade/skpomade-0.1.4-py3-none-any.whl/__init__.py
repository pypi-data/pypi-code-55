# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Valentin Emiya
"""
from .factorization_construction import direct_svd, evd_nystrom
from .range_approximation import \
    randomized_range_finder, adaptive_randomized_range_finder

# TODO replace RandomState by BitGenerator

__all__ = ['direct_svd', 'evd_nystrom',
           'randomized_range_finder', 'adaptive_randomized_range_finder']

__version__ = "0.1.4"
