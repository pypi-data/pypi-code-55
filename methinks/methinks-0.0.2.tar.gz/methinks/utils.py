import json
import datetime


def datetime_aware(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.strftime('%c')
    return o


def str_to_date(s):
    return datetime.datetime.strptime(s, '%c')


def data_to_json(data):
    return json.dumps(data, default=datetime_aware)
