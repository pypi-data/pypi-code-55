import datetime
import time


class tzoffset(datetime.tzinfo):

    def __init__(self, **kwargs):
        # Must initialise with seconds OR minutes OR hours, or with no arguments to get an offset of zero.
        if len(kwargs) > 1 or (len(kwargs) == 1 and not 'seconds' in kwargs and not 'hours' in kwargs and not 'minutes' in kwargs):
            raise Exception("tzoffset must be initialised with precisely one of 'seconds', 'minutes' or 'hours' keyword arguments")

        self._offset = datetime.timedelta(**kwargs)


    def utcoffset(self, dt):
        return self._offset

    def dst(self, dt):
        return datetime.timedelta()

    def tzname(self, dt):
        return None

    def __repr__(self):
        return "tzoffset(%s hours)" % (self._offset.total_seconds() / 3600)


# People should probably never use this, but we provide it for completeness.
class tzlocal(tzoffset):

    def __init__(self):
        if time.daylight:
            s = -time.altzone
        else:
            s = -time.timezone
        tzoffset.__init__(self, seconds=s)


    def __repr__(self):
        return "tzlocal(%s hour offset)" % (self._offset.total_seconds() / 3600)


class tzutc(tzoffset):

    def __init__(self):
        tzoffset.__init__(self, minutes=0)

    def __repr__(self):
        return "tzutc"

#!defModuleAttr(anvil.tz)!1: {name: 'UTC', type: 'any', description: 'An object representing the UTC timezone'}
UTC = tzutc()
