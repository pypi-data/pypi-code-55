import datetime
import re


def parse_range(rng):
    for x in rng.split(','):
        x = x.strip()
        if x.isdigit():
            yield int(x)
        elif '-' in x:
            xr = x.split('-')
            yield from range(int(xr[0].strip()), int(xr[1].strip()) + 1)
        elif '..' in x:
            xr = x.split('..')
            yield from range(int(xr[0].strip()), int(xr[1].strip()) + 1)
        else:
            raise ValueError(f"Unknown range specified: {x}")


def _re(variable, re):
    return f"((?P<{variable}>\\d+?)[ ]*({re}))?[ ,]*"


DURATION = re.compile(_re('hours', 'h|hrs?|hours?') + _re('minutes', 'm|mins?') + _re('seconds', 's|sec?'))


def is_num(x):
    return isinstance(x, (int, float, complex)) and not isinstance(x, bool)

def duration(t):
    if isinstance(t, datetime.timedelta):
        return t
    if is_num(t):
        return datetime.timedelta(seconds=t)
    if isinstance(t, str):
        return parse_duration(t)
    return None

def parse_duration(time_str):
    # print(time_str)
    parsed = DURATION.match(time_str.strip())
    if not parsed:
        return None
    params = {}
    for (name, param) in parsed.groupdict().items():
        if param:
            params[name] = int(param)
    if len(params) == 0:
        return None
    return datetime.timedelta(**params)


if __name__ == '__main__':
    print(parse_duration('1hour'))
    print(parse_duration('2 hours , 3 mins'))
    print(parse_duration('5h 3m'))
    print(parse_duration('1x'))
