from datetime import datetime, timedelta
from pytz import timezone
from dateutil import relativedelta
from .period_cursor import PeriodCursor
import re
from .period_timezone import PeriodTimezone

class PeriodIterator:
    def __init__(self, period, timezone_name):
        self.timezone_name = timezone_name
        self.timezone = timezone(timezone_name)
        self.now = datetime.now(self.timezone)
        tzfmt = PeriodTimezone()
        self.timezone_offset = tzfmt.format(self.now.strftime('%Z'))

        if period == 'lastonequarterhour':
            offsetFrom15 = self.now.minute % 15
            baseline = self.now - \
                relativedelta.relativedelta(minutes=-offsetFrom15)
            start = baseline + relativedelta.relativedelta(minutes=-15)
            end = baseline + relativedelta.relativedelta(minutes=-1)
            self.start = start.strftime(
                '%Y-%m-%dT%H:%M:00{}'.format(self.timezone_offset))
            self.end = end.strftime(
                '%Y-%m-%dT%H:%M:59{}'.format(self.timezone_offset))
        elif period == 'lasthour':
            baseline = self.now + relativedelta.relativedelta(hours=-1)
            self.start = baseline.strftime(
                '%Y-%m-%dT%H:00:00{}'.format(self.timezone_offset))
            self.end = baseline.strftime(
                '%Y-%m-%dT%H:59:59{}'.format(self.timezone_offset))
        elif period == 'today':
            self.start = self.now.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = self.now.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'daybeforeyesterday':
            daybeforeyesterday = self.now - timedelta(days=2)
            self.start = daybeforeyesterday.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = daybeforeyesterday.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'yesterday':
            yesterday = self.now - timedelta(days=1)
            self.start = yesterday.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = yesterday.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'thismonth':
            firstOfNextMonth = self.now.replace(day=1) + relativedelta.relativedelta(months=1)
            firstOfThisMonth = self.now.replace(day=1)
            endOfThisMonth = firstOfNextMonth + relativedelta.relativedelta(days=-1)
            self.start = firstOfThisMonth.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = endOfThisMonth.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'lastmonth':
            firstOfThisMonth = self.now.replace(day=1)
            endOfLastMonth = firstOfThisMonth + \
                relativedelta.relativedelta(days=-1)
            firstOfLastMonth = endOfLastMonth.replace(day=1)
            self.start = firstOfLastMonth.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = endOfLastMonth.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif "," in period:
            (start, end) = period.split(',', 2)
            startToken = PeriodIterator(start, timezone_name)
            endToken = PeriodIterator(end, timezone_name)
            self.start = startToken.start
            self.end = endToken.end
        elif re.match(r'^\d{4}-\d{2}-\d{2}$', period):
            self.start = '{d}T00:00:00{z}'.format(d = period, z=self.timezone_offset)
            self.end = '{d}T23:59:59{z}'.format(d = period, z=self.timezone_offset)
        else:
            self.start = period
            self.end = period
        self.cursorEnd = PeriodCursor(self.end, timezone_name)
        self.reset()

    def reset(self):
        self.cursor = PeriodCursor(self.start, self.timezone_name)

    def next(self):
        if self.cursor >= self.cursorEnd:
            return False
        self.cursor = self.cursor.tomorrow()
        return True
