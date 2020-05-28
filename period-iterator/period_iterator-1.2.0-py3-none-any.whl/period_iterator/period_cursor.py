from datetime import datetime
from dateutil import relativedelta
from .period_timezone import period_timezone
from pytz import timezone

class period_cursor:
    def __init__(self, timestamp, timezone_name):
        self.timezone_name = timezone_name
        self.timezone = timezone(timezone_name)
        self.now = datetime.now(self.timezone)
        tzfmt = period_timezone()
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
        return period_cursor((self.cursor + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S{}'.format(self.timezone_offset)), self.timezone_name)

    def begin(self, format='default'):
        if format=='default':
            return self.cursor.strftime('%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))
        return datetime.fromisoformat(self.cursor.strftime('%Y-%m-%dT00:00:00{}'.format(self.timezone_offset))).strftime(format)

    def end(self, format='default'):
        if format=='default':
            return self.cursor.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))
        return datetime.fromisoformat(self.cursor.strftime('%Y-%m-%dT23:59:59{}'.format(self.timezone_offset))).strftime(format)