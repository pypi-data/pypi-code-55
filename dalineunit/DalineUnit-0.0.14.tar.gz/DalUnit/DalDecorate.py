"""
@File    :   DalDecorate.py    
@Software:   PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/15 14:54  kun.z      1.0         None
"""

from functools import wraps
def gen_exception_decorate(obj_func):
    @wraps(obj_func)
    def wrapTheFunction(*args, **kwargs):
        try:
            return obj_func(*args, **kwargs)
        except Exception as e:
            # print(obj_func)
            # print(obj_func.__code__.co_filename)
            err_str = str(obj_func.__code__.co_filename) + str(obj_func.__class__) + str(obj_func.__name__)
            print("程序出错：设计文档 %s 报错，详情如下：%s"%(str(e), err_str))
            return str(e)
    return wrapTheFunction