import sys
import time
import traceback
from functools import wraps


# https://www.jianshu.com/p/ee82b941772a
def InterVal(start_time, interval):
    '''
    执行函数必须间隔多少时间,没有到指定的时间函数就不会被执行
    :param start_time: 传入开始时间
    :param interval: 秒数
    :return: 返回执行结果  否则返回 None
    '''

    def dewrapper(func):
        """
        它能把原函数的元信息拷贝到装饰器里面的 func 函数中。
        函数的元信息包括docstring、name、参数列表等等。可以尝试去除@functools.wraps(func)，
        你会发现test.__name__的输出变成了wrapper。
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = start_time
            time_now = int(time.time())
            if time_now - start > interval:
                result = func(*args, **kwargs)
                return result
            else:
                return None

        return wrapper

    return dewrapper


def timethis(func):
    """
    函数执行的时间差
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


def try_except(callback=None, is_print=True):
    def dewrapper(func):
        """
        使用装饰器使用try_except
        :param func:
        :return:
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except BaseException as e:
                if callback is not None:
                    callback(*sys.exc_info(), *args, **kwargs)
                if is_print:
                    print(traceback.format_exc())
                return None

        return wrapper

    return dewrapper
