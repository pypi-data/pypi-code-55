from functools import wraps

from flask import g, jsonify

from ForMark.ForLog import ForLog
from ForMark.ForString import is_none_str


def get_params(params=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if params:
                if not g.params:
                    return jsonify(success=False, msg='缺少必填参数', code='10001')
                for item in params.items():
                    value = g.params.get(item[0], None)
                    ForLog.show("参数", value)
                    if is_none_str(value):
                        return jsonify(success=False, msg=item[1], code='10001')

                    g.setdefault(item[0], value)
            return func(*args, **kwargs)

        return inner

    return wrapper
