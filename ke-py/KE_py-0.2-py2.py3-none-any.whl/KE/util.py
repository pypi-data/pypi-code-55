# coding=u8
import time
import warnings
from functools import wraps
from datetime import date, datetime, timedelta


def danger_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Be cautious! This is a dangerous action, the action will be executing after 10 Seconds')
        print('You can press Ctrl + C to cancel')
        time.sleep(10)
        return func(*args, **kwargs)
    return wrapper


def unify_timestamp(d):
    """Convert date, datetime to timestamp

    :param d: date or datetime
    :return: timestamp
    """
    if isinstance(d, datetime):
        timestamp = d.strftime('%s000')
        return timestamp
    if isinstance(d, date):
        dt = datetime.fromordinal(d.toordinal())
        timestamp = dt.strftime('%s000')
        return timestamp
    else:
        return d
