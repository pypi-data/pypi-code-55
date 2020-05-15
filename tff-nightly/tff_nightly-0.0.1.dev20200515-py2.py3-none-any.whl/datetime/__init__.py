# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Date-related utilities."""

from tf_quant_finance.datetime.constants import BusinessDayConvention
from tf_quant_finance.datetime.constants import Month
from tf_quant_finance.datetime.constants import PeriodType
from tf_quant_finance.datetime.constants import WeekDay
from tf_quant_finance.datetime.constants import WeekendMask

from tf_quant_finance.datetime.date_tensor import convert_to_date_tensor
from tf_quant_finance.datetime.date_tensor import DateTensor
from tf_quant_finance.datetime.date_tensor import from_datetimes as dates_from_datetimes
from tf_quant_finance.datetime.date_tensor import from_np_datetimes as dates_from_np_datetimes
from tf_quant_finance.datetime.date_tensor import from_ordinals as dates_from_ordinals
from tf_quant_finance.datetime.date_tensor import from_tensor as dates_from_tensor
from tf_quant_finance.datetime.date_tensor import from_tuples as dates_from_tuples
from tf_quant_finance.datetime.date_tensor import from_year_month_day as dates_from_year_month_day
from tf_quant_finance.datetime.date_tensor import random_dates
from tf_quant_finance.datetime.daycounts import actual_360 as daycount_actual_360
from tf_quant_finance.datetime.daycounts import actual_365_actual as daycount_actual_365_actual
from tf_quant_finance.datetime.daycounts import actual_365_fixed as daycount_actual_365_fixed
from tf_quant_finance.datetime.daycounts import thirty_360_isda as daycount_thirty_360_isda
from tf_quant_finance.datetime.holiday_calendar import HolidayCalendar
from tf_quant_finance.datetime.holiday_calendar_factory import create_holiday_calendar
from tf_quant_finance.datetime.periods import day
from tf_quant_finance.datetime.periods import days
from tf_quant_finance.datetime.periods import month
from tf_quant_finance.datetime.periods import months
from tf_quant_finance.datetime.periods import PeriodTensor
from tf_quant_finance.datetime.periods import week
from tf_quant_finance.datetime.periods import weeks
from tf_quant_finance.datetime.periods import year
from tf_quant_finance.datetime.periods import years
from tf_quant_finance.datetime.schedules import BusinessDaySchedule
from tf_quant_finance.datetime.schedules import PeriodicSchedule

from tensorflow.python.util.all_util import remove_undocumented  # pylint: disable=g-direct-tensorflow-import


_allowed_symbols = [
    'BusinessDayConvention',
    'BusinessDaySchedule',
    'DateTensor',
    'HolidayCalendar',
    'create_holiday_calendar',
    'Month',
    'PeriodType',
    'WeekDay',
    'WeekendMask',
    'convert_to_date_tensor',
    'dates_from_datetimes',
    'dates_from_np_datetimes',
    'dates_from_ordinals',
    'dates_from_tensor',
    'dates_from_tuples',
    'dates_from_year_month_day',
    'day',
    'days',
    'week',
    'weeks',
    'month',
    'months',
    'year',
    'years',
    'PeriodTensor',
    'PeriodicSchedule',
    'random_dates',
    'daycount_actual_360',
    'daycount_actual_365_actual',
    'daycount_actual_365_fixed',
    'daycount_thirty_360_isda',
]

remove_undocumented(__name__, _allowed_symbols)
