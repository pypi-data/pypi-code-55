import datetime
import hashlib
import json
import time
import traceback


def strtime(x=None):
    if not x:
        x = nowms()
    if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return strtime(datetime.datetime.fromtimestamp(x / 1000))


def nowStrAlignSecond():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def nowStrAlignDay():
    return datetime.datetime.now().strftime('%Y%m%d')


def nowms():
    return int(time.time() * 1000)


def nows():
    return int(time.time())


def formatException(err):
    return ''.join(traceback.TracebackException.from_exception(err).format())  # .replace('\\n', '\n')


def pretty(x):
    return json.dumps(x, indent=4, sort_keys=True, ensure_ascii=False)


def md5(key):
    m = hashlib.md5()
    m.update(key.encode())
    return m.hexdigest()