"""

"""

import time
import functools
import logging
import sys
import random
import traceback
import json

# 导入常用的固定路径(多平台通用)
from kw618._file_path import *


# 个人用于记录报错内容的log装饰器
def log_error(log_directory=f"{FILE_PATH_FOR_ZIRU_CODE}/Log/ttt_log"):
    # 作为装饰器时, 一定要加上(); 否则就不会返回内部的decorate函数了
    # 如果没有传入log的存放目录, 默认使用上述目录
    def decorate(func):
        def record_error(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                module_name = get_this_module_name()
                func_name = func.__name__ # 暂时没利用, 可删
                kprint(module_name=module_name, func_name=func_name)
                tb_txt = traceback.format_exc(limit=5) # limit参数: 表示traceback最多到第几层
                log_file_path = f"{log_directory}/{module_name}_error.log"
                with open(log_file_path, "a", encoding="utf-8") as f:
                    print(f"\n【捕获到异常】\n{tb_txt}\n【异常存储路径】: {log_file_path}\n")
                    log_msg = tb_txt
                    this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    f.write(f"{this_time}\n{log_msg}\n\n\n")
        return record_error
    return decorate



# python官网的例子
def logged(level, name=None, message=None):
    """
    这是python cookbook 中官方写写的log案例
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.

    可以看到, 如果你想要给装饰器传参, 就需要在decorate外面再嵌套一层函数: 总共3层
    """
    def decorate(func): # 此处一定只有一个func形参
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @functools.wraps(func) # 这里的装饰器可以修改__name__的问题(其实没啥用, 反正写上更好就对了, 管他呢)
        def wrapper(*args, **kwargs):  # 此处的形参一定是(*args, **kwargs), 并且与下面return中传入的参数一致!!
            log.log(level, logmsg)
            return func(*args, **kwargs) # 一定要记得return
        return wrapper  # 返回的函数名称一定和上面定义(warpper)的一致!!
    return decorate

# Example use
# @logged(logging.DEBUG)
# def add(x, y):
#     return x + y
#
# @logged(logging.CRITICAL, 'example')
# def spam():
#     print('Spam!')




def timer(func):
    """装饰器：记录并打印函数耗时"""
    def decorated(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print('执行时长: {} 秒'.format(time.time() - st))
        return ret
    return decorated



def get_this_module_name():
    "获取本函数所在脚本的模块名称"
    argv_str = sys.argv[-1]
    return argv_str.split("/")[-1][:-3]



def kprint(**kwargs):
    "方便打印出某些变量的值(测试使用); 需要使用关键字传参"
    json_ = json.dumps(kwargs, indent=4, ensure_ascii=False)
    print(json_)



def k_update(dic, key, value):
    "添加一个'k-v'对的同时, 返回这个添加后的dict对象!! (python默认是没有返回值的, 有些时候不方便) [下同]"
    dic[str(key)] = value
    return dic

def k_append(lst, element):
    lst.append(element)
    return lst

def k_extend(lst, lst2):
    lst.extend(lst2)
    return lst






if __name__ == "__main__":
    m = 33
    n = 99
    kprint(m=m, n=n)








#
