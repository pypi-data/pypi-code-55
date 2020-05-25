# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""

import pyvacon.analytics as _analytics
from pyvacon._converter import _add_converter

DiscountCurve = _add_converter(_analytics.DiscountCurve)
SurvivalCurve = _add_converter(_analytics.SurvivalCurve)
DividendTable = _add_converter(_analytics.DividendTable)
ForwardCurve = _add_converter(_analytics.ForwardCurve)
EquityForwardCurve = _add_converter(_analytics.EquityForwardCurve)
InflationIndexForwardCurve = _add_converter(_analytics.InflationIndexForwardCurve)
BaseDatedCurve = _add_converter(_analytics.BaseDatedCurve)
DatedCurve = _add_converter(_analytics.DatedCurve)
RatingTransitionBase = _add_converter(_analytics.RatingTransitionBase)
RatingTransition = _add_converter(_analytics.RatingTransition)
VolatilitySurface = _add_converter(_analytics.VolatilitySurface)
VolatilityParametrizationSSVI = _add_converter(_analytics.VolatilityParametrizationSSVI)

Rating = _add_converter(_analytics.Rating)
CalibrationStorage = _add_converter(_analytics.CalibrationStorage)
MarketDataManager = _add_converter(_analytics.MarketDataManager)
ParameterManager = _add_converter(_analytics.ParameterManager)

