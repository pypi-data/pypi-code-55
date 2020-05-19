# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""Top-level package for soapcw."""

__author__ = """Joe Bayley"""
__email__ = 'joseph.bayley@glasgow.ac.uk'
__version__ = '0.1.0'
from .soapcw import single_detector, two_detector, three_detector, single_detector_gaps
from .tools import tools, plots

from .line_aware_stat import __init__

#try:
#    from .lookup_table import gen_lookup_python, save_lookup, gen_lookup
#except:
#    from .lookup_table import gen_lookup_python, save_lookup

