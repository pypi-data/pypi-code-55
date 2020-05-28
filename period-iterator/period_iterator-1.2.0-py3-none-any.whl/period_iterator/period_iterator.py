from datetime import datetime, timedelta
from pytz import timezone
from dateutil import relativedelta
from .period_cursor import period_cursor
import re
from .period_timezone import period_timezone

class period_iterator:
    def __init__(self, period, timezone_name):
        self.timezone_name = timezone_name
        self.timezone = timezone(timezone_name)
        self.now = datetime.now(self.timezone)
        tzfmt = period_timezone()
        self.timezone_offset = tzfmt.format(self.now.strftime('%Z'))

        if period == 'lastonequarterhour':
            offset_from_15 = self.now.minute % 15
            baseline = self.now - \
                relativedelta.relativedelta(minutes=-offset_from_15)
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
            day_before_yesterday = self.now - timedelta(days=2)
            self.start = day_before_yesterday.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = day_before_yesterday.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'yesterday':
            yesterday = self.now - timedelta(days=1)
            self.start = yesterday.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = yesterday.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'thismonth':
            first_of_next_month = self.now.replace(day=1) + relativedelta.relativedelta(months=1)
            first_of_this_month = self.now.replace(day=1)
            end_of_this_month = first_of_next_month + relativedelta.relativedelta(days=-1)
            self.start = first_of_this_month.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = end_of_this_month.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif period == 'lastmonth':
            first_of_this_month = self.now.replace(day=1)
            end_of_last_month = first_of_this_month + \
                relativedelta.relativedelta(days=-1)
            first_of_last_month = end_of_last_month.replace(day=1)
            self.start = first_of_last_month.strftime(
                '%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
            self.end = end_of_last_month.strftime(
                '%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        elif "," in period:
            (start, end) = period.split(',', 2)
            start_token = period_iterator(start, timezone_name)
            end_token = period_iterator(end, timezone_name)
            self.start = start_token.start
            self.end = end_token.end
        elif re.match(r'^\d{4}-\d{2}-\d{2}$', period):
            self.start = '{d}T00:00:00{z}'.format(d = period, z=self.timezone_offset)
            self.end = '{d}T23:59:59{z}'.format(d = period, z=self.timezone_offset)
        else:
            self.start = period
            self.end = period
        self.cursor_end = period_cursor(self.end, timezone_name)
        self.reset()

    def reset(self):
        self.cursor = period_cursor(self.start, self.timezone_name)

    def next(self):
        if self.cursor >= self.cursor_end:
            return False
        self.cursor = self.cursor.tomorrow()
        return True

    def begin(self, format='default'):
        if format=='default':
            return self.start
        return datetime.fromisoformat(self.start).strftime(format)

    def end(self, format='default'):
        if format=='default':
            return self.end
        return datetime.fromisoformat(self.end).strftime(format)