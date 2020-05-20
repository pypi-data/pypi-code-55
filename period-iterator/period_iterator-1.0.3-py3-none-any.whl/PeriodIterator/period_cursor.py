from datetime import datetime
from dateutil import relativedelta
from .period_timezone import PeriodTimezone
from pytz import timezone

class PeriodCursor:
    def __init__(self, timestamp, timezone_name):
        self.timezone_name = timezone_name
        self.timezone = timezone(timezone_name)
        self.now = datetime.now(self.timezone)
        tzfmt = PeriodTimezone()
        self.timezone_offset = tzfmt.format(self.now.strftime('%Z'))

        self.cursor = datetime.fromisoformat(timestamp)
        self.comparableCursor = self.cursor.strftime('%Y-%m-%d')

    def __ge__(self, other):
        return self.comparableCursor >= other.comparableCursor

    def __eq__(self, other):
        return self.comparableCursor == other.comparableCursor

    def __repr__(self):
        return self.comparableCursor

    def tomorrow(self):
        return PeriodCursor((self.cursor + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S{}'.format(self.timezone_offset)), self.timezone_name)

    def begin(self):
        return self.cursor.strftime('%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))

    def end(self):
        return self.cursor.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))