# -*- coding:utf-8 -*-
import skydl
from skydl.common.annotations import print_exec_time
from skydl.cython.examples.demo.cdemo import PyCythonDemo
from skydl.cython.examples.mcpp.test.container_unit_tests import (
    run_emplace_object_move_vector
)
from skydl.cython.common.common import PyCommon, PyTimerUtil


@print_exec_time
def cython_smoke_test():
    py_timer_util = PyTimerUtil("cython_smoke_test", True, time_unit="nanoseconds")
    print("begin to cython smoke testing......")
    py_timer_util.start_timer()
    ret = run_emplace_object_move_vector()
    print(f"mcpp testing......ret={ret}")
    demo = PyCythonDemo(100)
    print(f"100+demo.add(1,199)={demo.add(1, 199)}")
    print(f"demo.mul(2)={demo.mul(2)}")
    print(f"demo.sayHello(b'HuaChao')={demo.sayHello(b'HuaChao')}")
    print(f"demo.sayHelloWithStr('HuaChao123')={demo.sayHelloWithStr('沈xx...')}")
    cython_count_down(demo)
    python_count_down()
    py_timer_util.stop_timer()
    print("now sleep 1 microseconds......")
    PyTimerUtil.sleep(1, "microseconds")
    print("cython smoke testing is succ!!!")


@print_exec_time
def cython_count_down(py_cython_demo, count=22000):
    py_cython_demo.countdown(count)


@print_exec_time
def python_count_down(count=22000):
    while count > 1:
        count -= 1


if __name__ == '__main__':
    print(f"cython...skydl c++ core version: {PyCommon().get_version()}, skydl python version：{skydl.__version__}")
    cython_smoke_test()
