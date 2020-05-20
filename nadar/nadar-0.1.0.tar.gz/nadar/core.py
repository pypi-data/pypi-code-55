import datetime
import re
from functools import singledispatch
from typing import Optional, Union
import dateparser

from nadar.helper import (
    DATE_FORMAT,
    FlexDate,
    Optional,
    SmartDate,
    SmartPeriod,
    Union,
    _delta_date_date,
    _delta_date_smart_date,
    _delta_date_str,
    _get_day_start,
    _get_day_start_date,
    _get_day_start_smart_date,
    _get_day_start_str,
    _get_decade_start,
    _get_decade_start_date,
    _get_decade_start_smart_date,
    _get_decade_start_str,
    _get_eo_day,
    _get_eo_day_date,
    _get_eo_day_smart_date,
    _get_eo_day_str,
    _get_eo_decade,
    _get_eo_decade_date,
    _get_eo_decade_smart_date,
    _get_eo_decade_str,
    _get_eo_fortnight,
    _get_eo_fortnight_date,
    _get_eo_fortnight_smart_date,
    _get_eo_fortnight_str,
    _get_eo_month,
    _get_eo_month_date,
    _get_eo_month_smart_date,
    _get_eo_month_str,
    _get_eo_quarter,
    _get_eo_quarter_date,
    _get_eo_quarter_smart_date,
    _get_eo_quarter_str,
    _get_eo_week,
    _get_eo_week_date,
    _get_eo_week_smart_date,
    _get_eo_week_str,
    _get_eo_year,
    _get_eo_year_date,
    _get_eo_year_smart_date,
    _get_eo_year_str,
    _get_fortnight_start,
    _get_fortnight_start_date,
    _get_fortnight_start_smart_date,
    _get_fortnight_start_str,
    _get_month_start,
    _get_month_start_date,
    _get_month_start_smart_date,
    _get_month_start_str,
    _get_quarter_start,
    _get_quarter_start_date,
    _get_quarter_start_smart_date,
    _get_quarter_start_str,
    _get_week_start,
    _get_week_start_date,
    _get_week_start_smart_date,
    _get_week_start_str,
    _get_year_start,
    _get_year_start_date,
    _get_year_start_smart_date,
    _get_year_start_str,
    _parse_ago,
    _parse_between,
    _parse_last,
    _parse_next,
    _parse_time_period,
    _text2int,
    dateparser,
    datetime,
    delta_date,
)


def get_start(period, reference_date: Optional[FlexDate] = None, strfdate="%Y-%m-%d") -> FlexDate:
    """
    Returns the first day of the given period for the reference_date.
    Period can be one of the following: {'year', 'quarter', 'month', 'week'}
    If reference_date is instance of str, returns a string.
    If reference_date is instance of datetime.date, returns a datetime.date instance.
    If reference_date is instance of SmartDate, returns a SmartDate instance.
    If no reference_date given, returns a SmartDate instance.

    Examples
    --------
    >>> # when no reference is given assume that it is datetime.date(2018, 5, 8)
    >>> get_start('month')
    SmartDate(2018, 5, 1)

    >>> get_start('quarter', '2017-05-15')
    '2017-04-01'

    >>> get_start('year', datetime.date(2017, 12, 12))
    datetime.date(2017, 01, 01)

    """

    start_functions = {
        "decade": _get_decade_start,
        "year": _get_year_start,
        "quarter": _get_quarter_start,
        "month": _get_month_start,
        "fortnight": _get_fortnight_start,
        "week": _get_week_start,
        "day": _get_day_start,
        "decades": _get_decade_start,
        "years": _get_year_start,
        "quarters": _get_quarter_start,
        "months": _get_month_start,
        "fortnights": _get_fortnight_start,
        "weeks": _get_week_start,
        "days": _get_day_start,
    }

    return start_functions[period](reference_date or SmartDate.today(), strfdate)


def get_end(period, reference_date: FlexDate, strfdate="%Y-%m-%d") -> FlexDate:
    """
    Returns the last day of the given period for the reference_date.
    Period can be one of the following: {'year', 'quarter', 'month', 'week'}
    If reference_date is instance of str, returns a string.
    If reference_date is instance of datetime.date, returns a datetime.date instance.
    If reference_date is instance of SmartDate, returns a SmartDate instance.
    If no reference_date given, returns a SmartDate instance.

    Examples
    --------
    >>> # when no reference is given assume that it is datetime.date(2018, 5, 8)
    >>> get_end('month')
    SmartDate(2018, 5, 31)

    >>> get_end('quarter', '2017-05-15')
    '2017-06-30'

    >>> get_end('year', '2017-12-12')
    datetime.date(2017, 12, 31)
    """
    end_functions = {
        "decade": _get_eo_decade,
        "year": _get_eo_year,
        "quarter": _get_eo_quarter,
        "month": _get_eo_month,
        "fortnight": _get_eo_fortnight,
        "week": _get_eo_week,
        "day": _get_eo_day,
        "decades": _get_eo_decade,
        "years": _get_eo_year,
        "quarters": _get_eo_quarter,
        "months": _get_eo_month,
        "fortnights": _get_eo_fortnight,
        "weeks": _get_eo_week,
        "days": _get_eo_day,
    }

    return end_functions[period](reference_date, strfdate)


# parse date
def parse_reference(date_string: str, reference: Optional[FlexDate] = None) -> SmartDate:
    """
    Takes in a string representing a delta in date and returns it given the reference date.

    Examples
    --------
    >>> # when no reference is given assume that it is datetime.date(2018, 5, 8)
    >>> parse_reference('one year ago')
    SmartDate(2017, 5, 8)

    >>> parse_reference('hace tres meses')
    SmartDate(2018, 2, 8)
    """
    reference = reference or datetime.date.today()

    # initialize start_date & end_date
    parsed_date = datetime.date.today()

    # take the period, remove all '_' and split it into the individual words:
    period_words = date_string.lower().replace("_", " ").split()

    # prepare different use cases:
    # one word input
    if len(period_words) == 1:
        matches = {"yesterday": -1, "today": 0, "tomorrow": 1}

        if period_words[0] in matches:
            return SmartDate.from_date(delta_date(reference, days=matches[period_words[0]]))
        if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", period_words[0]):
            return SmartDate.from_date(
                datetime.datetime.strptime(period_words[0], "%Y-%m-%d").date()
            )
        else:
            try:
                return SmartDate.from_date(dateparser.parse(date_string).date())
            except Exception:
                raise TypeError("The period '%s' could not be recognized." % period_words)

    else:

        if date_string.endswith("ago"):
            # check if the first part of the string is a figure information and convert it to an integer

            number, time_period = _parse_ago(date_string)

            return SmartDate.from_date(delta_date(reference, **{time_period: -number}))

    #                raise TypeError("The period doesn't include a supported time period which should be '<figure> "
    #                                "<day|week|fortnight|month|quarter|year|decade>(s) ago'.")
    try:
        return SmartDate.from_date(dateparser.parse(date_string).date())
    except Exception:
        pass


def parse_period(period_string: str, reference: Optional[FlexDate] = None) -> SmartPeriod:
    """
    Takes in a string representing a period and returns it given the reference date.

    Examples
    --------

    >>> # when no reference is given assume that it is datetime.date(2018, 5, 8)
    >>> parse_period('last month')
    SmartPeriod(SmartDate(2018, 4, 1), SmartDate(2018, 4, 30))

    >>> parse_period('this week')
    SmartPeriod(SmartDate(2018, 5, 7), SmartDate(2018, 5, 13))

    >>> parse_period('last year', reference='2017-10-28')
    SmartPeriod(SmartDate(2016, 1, 1), SmartDate(2016, 12, 31))

    >>> parse_period('last quarter', reference=SmartDate(2017, 5, 3))
    SmartPeriod(SmartDate(2017, 1, 1), SmartDate(2017, 3, 31))
    """
    reference = reference or datetime.date.today()

    if isinstance(period_string, tuple):
        start_date = datetime.datetime.strptime(period_string[0], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(period_string[1], "%Y-%m-%d").date()

    else:

        if period_string == "":
            return parse_period("yesterday", reference)

        # take the period, remove all '_' and split it into the individual words:
        period_words = period_string.lower().replace("_", " ").split()

        if len(period_words) == 1:
            if period_words[0].endswith("td"):
                period_words = ["this", period_words[0][0:-2]]
            elif period_words[0] == "today":
                period_words = ["this", "day"]
            elif period_words[0].startswith("t"):
                period_words = ["this", period_words[0][1:]]
            elif re.fullmatch(r"^l(\d+)(dec|d|w|m|q|y|f)$", period_words[0]):
                number, time_period = re.match(
                    r"^l(\d+)(dec|d|w|m|q|y|f)$", period_words[0]
                ).groups()
                period_words = ["last", number, time_period]
                period_string = " ".join(period_words)
            elif re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", period_words[0]):

                start_date = end_date = datetime.datetime.strptime(
                    period_words[0], "%Y-%m-%d"
                ).date()
                return SmartPeriod(SmartDate.from_date(start_date), SmartDate.from_date(end_date))
            elif period_words[0] == "yesterday":
                start_date = end_date = delta_date(reference, days=-1)
                return SmartPeriod(SmartDate.from_date(start_date), SmartDate.from_date(end_date))

        # 'this'cases
        if period_words[0] in ["this", "t"] and len(period_words) == 2:
            time_period = _parse_time_period(period_words[-1])
            start_date = get_start(time_period, reference)
            if time_period == "days":
                end_date = reference
            else:
                end_date = parse_reference("yesterday", reference)

            # end_date = get_end(time_period, reference)

        elif (
            period_words[-1] == "date"
            and period_words[-2] == "to"
            and period_words[0]
            in ["day", "week", "fortnight", "month", "quarter", "year", "decade"]
        ):
            return parse_period("this " + period_words[0], reference=reference)

        # 'last' cases
        elif "last" in period_words or "l" in period_words:
            if period_words[-2] in ["last", "l"] and period_words[-1] == "year":
                time_period = _parse_time_period(period_words[-1])

                if len(period_words) > 2:
                    return parse_period(
                        " ".join(period_words[:-2]), delta_date(reference, **{time_period: -1})
                    )
                else:
                    start_date = get_start(time_period, delta_date(reference, **{time_period: -1}))
                    end_date = get_end(time_period, delta_date(reference, **{time_period: -1}))
            elif period_words[0] in ["last", "l"]:
                number, time_period = _parse_last(period_string)

                start_date = get_start(time_period, delta_date(reference, **{time_period: -number}))
                if time_period == "fortnights":
                    end_date = get_end("weeks", delta_date(reference, weeks=-1))
                else:
                    end_date = get_end(time_period, delta_date(reference, **{time_period: -1}))

        # 'next' cases
        elif period_words[0] in ["next", "n"]:
            # check if the middle part of the string is a figure information and convert it to an integer

            number, time_period = _parse_next(period_string)

            start_date = get_start(time_period, delta_date(reference, **{time_period: 1}))
            end_date = get_end(time_period, delta_date(reference, **{time_period: number}))

        # 'between x and Y <time period> ago' cases
        elif period_words[-1] in ["ago"]:
            if period_words[0] in ["between"]:

                x_number, y_number, time_period = _parse_between(period_string)

                start_date = delta_date(reference, **{time_period: -x_number})
                end_date = delta_date(reference, **{time_period: -y_number})

            else:
                number, time_period = _parse_ago(period_string)

                start_date = get_start(time_period, delta_date(reference, **{time_period: -number}))
                end_date = get_end(time_period, delta_date(reference, **{time_period: -number}))

        else:
            start_date = parse_reference(period_string, reference)
            _, time_period = _parse_ago(period_string)
            end_date = delta_date(start_date, **{time_period: 1}, days=-1)

    if end_date < start_date:
        end_date = start_date

    return SmartPeriod(SmartDate.from_date(start_date), SmartDate.from_date(end_date))


def smart_dates(period, reference=(), datetime_format=False):
    """Wrapper that implements EMEA's smart_date"""
    if not reference:
        if datetime_format:
            return parse_period(period).to_date()
        else:
            return parse_period(period).to_string()
    elif isinstance(reference, str):
        if datetime_format:
            return parse_period(period, parse_reference(reference)).to_date()
        else:
            return parse_period(period, parse_reference(reference)).to_string()
    elif isinstance(reference, datetime.date):
        if datetime_format:
            return parse_period(period, parse_reference(reference.strftime("%Y-%m-%d"))).to_date()
        else:
            return parse_period(period, parse_reference(reference.strftime("%Y-%m-%d"))).to_string()
    else:
        if datetime_format:
            return [
                parse_period(period, parse_reference(reference)).to_date()
                for reference in reference
            ]

        else:
            return [
                parse_period(period, parse_reference(reference)).to_string()
                for reference in reference
            ]
