import datetime
import re
from functools import singledispatch
from typing import Optional, Union
import dateparser

DATE_FORMAT = "%Y-%m-%d"


class SmartDate(datetime.date):
    def __new__(cls, year, month, day, format="%Y-%m-%d"):
        self = datetime.date.__new__(cls, year=year, month=month, day=day)

        self._format = format
        return self

    def __str__(self):
        return self.strftime(self._format)

    def __repr__(self):
        return f"SmartDate({self.__str__()})"

    @classmethod
    def today(cls, format="%Y-%m-%d"):
        _today = datetime.date.today()
        return cls(_today.year, _today.month, _today.day, format=format)

    @classmethod
    def from_date(cls, _date, format="%Y-%m-%d"):
        return cls(_date.year, _date.month, _date.day, format=format)

    def to_date(self):
        return datetime.date(self.year, self.month, self.day)

    @property
    def strfdate(self):
        return self._format


class SmartPeriod:
    def __init__(self, start_date: SmartDate, end_date: SmartDate):
        self._start_date = start_date
        self._end_date = end_date

    def __repr__(self):
        return f"SmartPeriod({self._start_date}, {self._end_date})"

    @property
    def start(self):
        return self._start_date

    @property
    def end(self):
        return self._end_date

    def to_string(self):
        return str(self._start_date), str(self._end_date)

    def to_date(self):
        return self._start_date.to_date(), self._end_date.to_date()

    def __iter__(self):
        for date in (self._start_date, self._end_date):
            yield date

    def __eq__(self, other):
        return self._start_date == other.start and self._end_date == other.end


FlexDate = Union[SmartDate, datetime.date, str]


# date modifier functions
@singledispatch
def delta_date(
    date_to_modify: FlexDate,
    days=0,
    weeks=0,
    fortnights=0,
    months=0,
    quarters=0,
    years=0,
    decades=0,
    strfdate="%Y-%m-%d",
) -> FlexDate:
    """
    Returns a date with +/- days/weeks/months/years.
    If date_to_modify is instance of str, returns a string.
    If date_to_modify is instance of datetime.date, returns a datetime.date instance.
    If date_to_modify is instance of SmartDate, returns a SmartDate instance.
    """

    raise NotImplementedError


@delta_date.register(str)
def _delta_date_str(
    date_to_modify,
    days=0,
    weeks=0,
    fortnights=0,
    months=0,
    quarters=0,
    years=0,
    decades=0,
    strfdate="%Y-%m-%d",
):
    return delta_date(
        datetime.datetime.strptime(date_to_modify, strfdate),
        days,
        weeks,
        fortnights,
        months,
        quarters,
        years,
        decades,
    ).strftime(strfdate)


@delta_date.register(SmartDate)
def _delta_date_smart_date(
    date_to_modify,
    days=0,
    weeks=0,
    fortnights=0,
    months=0,
    quarters=0,
    years=0,
    decades=0,
    strfdate="%Y-%m-%d",
):
    return SmartDate.from_date(
        delta_date(
            date_to_modify.to_date(), days, weeks, fortnights, months, quarters, years, decades
        )
    )


@delta_date.register(datetime.date)
def _delta_date_date(
    date_to_modify,
    days=0,
    weeks=0,
    fortnights=0,
    months=0,
    quarters=0,
    years=0,
    decades=0,
    strfdate="%Y-%m-%d",
):
    new_year = date_to_modify.year + years + decades * 10
    new_month = date_to_modify.month + months + quarters * 3
    start_day = date_to_modify.day

    if new_month < 1:
        while new_month < 1:
            new_year -= 1
            new_month += 12
    elif new_month > 12:
        while new_month > 12:
            new_year += 1
            new_month -= 12

    try:
        new_date = datetime.datetime(year=new_year, month=new_month, day=start_day)
    except ValueError:
        new_date = _get_eo_month(datetime.datetime(year=new_year, month=new_month, day=1))

    temp_date = new_date + datetime.timedelta(days=days + weeks * 7 + fortnights * 14)
    return datetime.date(temp_date.year, temp_date.month, temp_date.day)


# date reference functions


@singledispatch
def _get_decade_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_decade_start.register(datetime.date)
def _get_decade_start_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return datetime.date(date.year - date.year % 10, 1, 1)


@_get_decade_start.register(str)
def _get_decade_start_str(date, strfdate="%Y-%m-%d") -> str:
    return _get_decade_start(datetime.datetime.strptime(date, strfdate).date()).strftime(strfdate)


@_get_decade_start.register(SmartDate)
def _get_decade_start_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return SmartDate.from_date(_get_decade_start(date.to_date()), date.strfdate)


@singledispatch
def _get_year_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_year_start.register(str)
def _get_year_start_str(date, strfdate):
    return _get_year_start(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_year_start.register(datetime.date)
def _get_year_start_date(date, strfdate="%Y-%m-%d"):
    return datetime.date(date.year, 1, 1)


@_get_year_start.register(SmartDate)
def _get_year_start_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_year_start(date.to_date()), date.strfdate)


@singledispatch
def _get_quarter_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_quarter_start.register(str)
def _get_quarter_start_str(date, strfdate):
    return _get_quarter_start(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_quarter_start.register(SmartDate)
def _get_quarter_start_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_quarter_start(date.to_date()), date.strfdate)


@_get_quarter_start.register(datetime.date)
def _get_quarter_start_date(date, strfdate="%Y-%m-%d"):
    return datetime.date(date.year, (date.month - 1) // 3 * 3 + 1, 1)


@singledispatch
def _get_month_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_month_start.register(str)
def _get_month_start_str(date, strfdate) -> str:
    return _get_month_start(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_month_start.register(datetime.date)
def _get_month_start_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return datetime.date(date.year, date.month, 1)


@_get_month_start.register(SmartDate)
def _get_month_start_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_month_start(date.to_date()), date.strfdate)


@singledispatch
def _get_fortnight_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_fortnight_start.register(datetime.date)
def _get_fortnight_start_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return get_start("week", date)


@_get_fortnight_start.register(str)
def _get_fortnight_start_str(date, strfdate="%Y-%m-%d") -> str:
    return _get_fortnight_start(datetime.datetime.strptime(date, strfdate).date()).strftime(
        strfdate
    )


@_get_fortnight_start.register(SmartDate)
def _get_fortnight_start_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return SmartDate.from_date(_get_fortnight_start(date.to_date()), date.strfdate)


@singledispatch
def _get_week_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_week_start.register(str)
def _get_week_start_str(date, strfdate="%Y-%m-%d"):
    return _get_week_start(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_week_start.register(datetime.date)
def _get_week_start_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return date - datetime.timedelta(days=date.weekday())


@_get_week_start.register(SmartDate)
def _get_week_start_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_week_start(date.to_date()), date.strfdate)


@singledispatch
def _get_day_start(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_day_start.register(datetime.date)
def _get_day_start_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return date


@_get_day_start.register(str)
def _get_day_start_str(date, strfdate="%Y-%m-%d") -> str:
    return date


@_get_day_start.register(SmartDate)
def _get_day_start_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return date


@singledispatch
def _get_eo_decade(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_decade.register(datetime.date)
def _get_eo_decade_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return datetime.date(date.year + date.year % 10, 12, 31)


@_get_eo_decade.register(str)
def _get_eo_decade_str(date, strfdate="%Y-%m-%d") -> str:
    return _get_eo_decade(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_decade.register(SmartDate)
def _get_eo_decade_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return SmartDate.from_date(_get_eo_decade(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_year(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_year.register(str)
def _get_eo_year_str(date, strfdate="%Y-%m-%d") -> str:
    return _get_eo_year(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_year.register(datetime.date)
def _get_eo_year_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return datetime.date(date.year, 12, 31)


@_get_eo_year.register(SmartDate)
def _get_eo_year_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return SmartDate.from_date(_get_eo_year(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_quarter(date):
    raise NotImplementedError


@_get_eo_quarter.register(datetime.date)
def _get_eo_quarter_date(date, strfdate="%Y-%m-%d"):
    return _get_eo_month(datetime.date(date.year, ((date.month - 1) // 3 + 1) * 3, 1))


@_get_eo_quarter.register(str)
def _get_eo_quarter_str(date, strfdate):
    return _get_eo_quarter(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_quarter.register(SmartDate)
def _get_eo_quarter_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_eo_quarter(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_month(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_month.register(str)
def _get_eo_month_str(date, strfdate):
    return _get_eo_month(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_month.register(datetime.date)
def _get_eo_month_date(date, strfdate="%Y-%m-%d"):
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


@_get_eo_month.register(SmartDate)
def _get_eo_month_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_eo_month(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_fortnight(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_fortnight.register(datetime.date)
def _get_eo_fortnight_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return _get_eo_week(date, strfdate)


@_get_eo_fortnight.register(str)
def _get_eo_fortnight_str(date, strfdate) -> str:
    return _get_eo_fortnight(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_fortnight.register(SmartDate)
def _get_eo_fortnight_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_eo_fortnight(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_week(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_week.register(datetime.date)
def _get_eo_week_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return _get_week_start(date) + datetime.timedelta(days=6)


@_get_eo_week.register(str)
def _get_eo_week_str(date, strfdate) -> str:
    return _get_eo_week(datetime.datetime.strptime(date, strfdate)).strftime(strfdate)


@_get_eo_week.register(SmartDate)
def _get_eo_week_smart_date(date, strfdate="%Y-%m-%d"):
    return SmartDate.from_date(_get_eo_week(date.to_date()), date.strfdate)


@singledispatch
def _get_eo_day(date, strfdate="%Y-%m-%d"):
    raise NotImplementedError


@_get_eo_day.register(datetime.date)
def _get_eo_day_date(date, strfdate="%Y-%m-%d") -> datetime.date:
    return date


@_get_eo_day.register(str)
def _get_eo_day_str(date, strfdate="%Y-%m-%d") -> str:
    return date


@_get_eo_day.register(SmartDate)
def _get_eo_day_smart_date(date, strfdate="%Y-%m-%d") -> SmartDate:
    return date


def _parse_time_period(s):
    if s in ["day", "days", "d", ""]:
        return "days"
    elif s in ["week", "weeks", "w"]:
        return "weeks"
    elif s in ["month", "months", "m"]:
        return "months"
    elif s in ["quarter", "quarters", "q"]:
        return "quarters"
    elif s in ["year", "years", "y"]:
        return "years"
    elif s in ["decade", "decades", "dec"]:
        return "decades"
    elif s in ["fortnight", "fortnights", "f"]:
        return "fortnights"
    else:
        raise TypeError(
            "The period doesn't include a supported time period which should be 'this "
            "<day|week|month|quarter|year|decade>'. '" + s + "' Given"
        )


def _parse_ago(date_string):

    period_words = date_string.lower().replace("_", " ").split()

    if len(period_words) == 3:
        number = int(period_words[0]) if period_words[0].isdigit() else _text2int(period_words[0])
    elif len(period_words) == 2:
        if period_words[0] in ["week", "month", "year", "quarter", "decade", "fortnight"]:
            number = 1
        else:
            raise TypeError(
                "The period doesn't include the correct information which should be '<figure> "
                "<time period> ago'."
            )
    else:
        try:
            number = _text2int(" ".join(period_words[0:-2]))
        except ValueError:
            raise TypeError("There is a typo in the written out integers in '%s'." % date_string)

    return number, _parse_time_period(period_words[-2])


def _parse_last(period_string):
    period_words = period_string.lower().replace("_", " ").split()

    # check if the middle part of the string is a figure information and convert it to an integer
    if len(period_words) == 3:
        if bool(re.search(r"\d", period_words[1])):
            number = int(period_words[1])
        else:
            number = _text2int(period_words[1])
    elif len(period_words) == 2:
        if period_words[-1] in ["week", "month", "year", "quarter", "decade", "fortnight", "day"]:
            number = 1
        else:
            raise TypeError(
                "The period doesn't include the correct information which should be 'last <figure> "
                "<time period>s'."
            )
    else:
        number = _text2int(" ".join(period_words[1:-1]))

    time_period = _parse_time_period(period_words[-1])

    return number, time_period


def _parse_next(period_string):
    period_words = period_string.lower().replace("_", " ").split()
    if len(period_words) == 3:
        if bool(re.search(r"\d", period_words[1])):
            number = int(period_words[1])
        else:
            number = _text2int(period_words[1])
    elif len(period_words) == 2:
        if period_words[-1] in ["week", "month", "year", "quarter", "decade", "fortnight", "day"]:
            number = 1
        else:
            raise TypeError(
                "The period doesn't include the correct information which should "
                "be 'last <figure> <time period>s'."
            )
    else:
        number = _text2int(" ".join(period_words[1:-1]))

    time_period = _parse_time_period(period_words[-1])

    return number, time_period


def _parse_between(period_string):
    period_words = period_string.lower().replace("_", " ").split()
    # extract the two numbers plus the period signal word
    if "and" in period_words[1:-2]:
        and_position = period_words[1:-2].index("and")
        x = period_words[1 : and_position + 1]
        y = period_words[(and_position + 2) : -2]
        if len(x) == 1:
            if bool(re.search(r"\d", x[0])):
                x_number = int(x[0])
            else:
                x_number = _text2int(x[0])
        else:
            try:
                x_number = _text2int(" ".join(x))
            except ValueError:
                raise TypeError(
                    "There is a typo in the written out integers in '%s'." % " ".join(x)
                )
        if len(y) == 1:
            if bool(re.search(r"\d", y[0])):
                y_number = int(y[0])
            else:
                y_number = _text2int(y[0])
        else:
            try:
                y_number = _text2int(" ".join(y))
            except ValueError:
                raise TypeError(
                    "There is a typo in the written out integers in '%s'." % " ".join(y)
                )
        if x_number < y_number:
            raise TypeError("An error occurred. The start date is earlier than the end date.")
    else:
        raise TypeError(
            "The period '%s' doesn't specify a correct start and end when when using 'between'."
            % period_string
        )

    time_period = _parse_time_period(period_words[-2])

    return x_number, y_number, time_period


def _text2int(text_num, num_words=None):
    """
    Function that takes an input string of a written number (in English) to translate it to
    the respective integer.
    :param text_num: string of a written number (in English)
    :param num_words: optional dictionary to add containing text number (keys) and respective digit
        (values) pairs
    :return: integer of the respective number
    """
    if num_words is None:
        num_words = dict()
        units = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
        ]

        tens = [
            "",
            "",
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
            "ninety",
        ]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        num_words["and"] = (1, 0)
        for idx, word in enumerate(units):
            num_words[word] = (1, idx)
        for idx, word in enumerate(tens):
            num_words[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            num_words[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in text_num.split():
        if word not in num_words:
            raise Exception("Illegal word: " + word)

        scale, increment = num_words[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
