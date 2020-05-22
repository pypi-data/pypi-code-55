import datetime
import decimal
import json
import numpy as np
import uuid

int_types = (
    np.int_, np.intc, np.intp, np.int8,
    np.int16, np.int32, np.int64, np.uint8,
    np.uint16, np.uint32, np.uint64
)

float_types = (
    np.float_, np.float16, np.float32, np.float64
)


def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def duration_iso_string(duration):
    if duration < datetime.timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = '.{:06d}'.format(microseconds) if microseconds else ""
    return '{}P{}DT{:02d}H{:02d}M{:02d}{}S'.format(sign, days, hours, minutes, seconds, ms)


# pylint: disable=too-many-return-statements,method-hidden,no-else-return
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, int_types):
            return int(o)
        elif isinstance(o, float_types):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        elif isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)
        else:
            pass

        return json.JSONEncoder.default(self, o)


def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v)) for k, v in dictionary.items())


def jsonify(data):
    if not data:
        return None

    data = convert_keys_to_string(data)

    return json.dumps(data, cls=JSONEncoder)
