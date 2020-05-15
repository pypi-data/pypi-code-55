# -*- coding:utf-8 -*-
import skydl
from skydl.pybind11.examples.demo import cdemo
from skydl.cython.common.common import PyCommon
from skydl.common.annotations import print_exec_time


@print_exec_time
def pybind11_smoke_test():
    pet = cdemo.Pet("沈", 12)
    pet.go_for_a_walk()
    print(f"cdemo.add(1,3)={cdemo.add(1, 23)}, pet.get_hunger()={pet.get_hunger()}")
    print("pybind11 smoke testing is succ!!!")


if __name__ == '__main__':
    print(f"pybind11...skydl c++ core version: {PyCommon().get_version()}, skydl python version：{skydl.__version__}")
    pybind11_smoke_test()

