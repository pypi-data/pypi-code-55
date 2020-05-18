from distutils.core import setup, Extension
# from setuptools import setup
from Cython.Build import cythonize
import os
import numpy

##########
lib_name = "skydlcython"
pkg_dir = "cython/examples"
modules = []  # ["cython_simple.pyx", "masked_log.pyx"]
install_requires = [
    "cython==0.29.15",
    "numpy>=1.17.3"
]
include_dirs = [numpy.get_include()]
###########

# dependencies
try:
    #import scipy  # noqa
    modules.append(
        Extension(lib_name, sources=[os.path.join(pkg_dir, "cdemo.pyx")], language='c++')
    )
    #install_requires.append("scipy")
except ImportError as e:  # noqa
    pass

modules = [module for module in modules]

setup(
    name=lib_name,
    version="0.0.1",
    description="Cython for skydl",
    packages=[pkg_dir],
    ext_modules=cythonize(modules),
    install_requires=install_requires,
    include_dirs=include_dirs)

# https://github.com/cython/cython
# 参考：Distributing python packages protected with Cython https://medium.com/swlh/distributing-python-packages-protected-with-cython-40fc29d84caf
# Using C++ in Cython https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html
# Cython的用法以及填坑姿势 https://blog.csdn.net/ios99999/article/details/77922410
# install cython 0.29.15 $pip3 install -U cython=0.29.15
# ref:Python3.X使用Cython调用C/C++ https://blog.csdn.net/huachao1001/article/details/88253977
# ref:Cython 3.0 中文文档 https://www.bookstack.cn/read/cython-doc-zh/README.md
# ref:https://github.com/ray-project/ray/tree/10f21fa313d8ee8cd636b1e945b1a02893d303f8/doc/examples/cython
# ref:CMAKE（3）—— aux_source_directory包含目录下所有文件以及自动构建系统 https://blog.csdn.net/u012564117/article/details/95085360
# ref:人生苦短，我用Cython！论用Cython加速Python并行计算的实践 https://cloud.tencent.com/developer/news/314117
# 1. $cd /Users/tony/myfiles/spark/share/cc-projects/hello-cmake
# 2. >>python3 hello/cython/examples/setup_cython_call_cc.py build_ext --inplace
#    或>>python3 hello/cython/examples/setup_cython_call_cc.py clean --all
# 3. 在生成的adapter.cython-36m-darwin.so所在的目录路径下测试python代码
# >> python3
# >>>from skydl.cython.examples.adapter import PyCythonDemo
# >>>demo=PyCythonDemo(100)
# >>>demo.add(1)
# 101
# >>>demo.mul(2)
# 200
# >>>demo.sayHello1(b'HuaChao')
# hello HuaChao
# >>>m=1000000000
# >>>demo.countdown(m)
# 用c++实现的countdown函数可以和以下纯python代码比较性能
# >>>while (m > 1): m -= 1
# 4. 或者打包成本机全局的安装包(install for source code)
# ========= 命令行如下 ===========
# $ python3 cython/examples/setup_cython_call_cc.py clean --all install --record cython/examples/setup_cython_call_cc_install_info.txt
#  生成的adapter.cpp文件可以手动删除
# 5. 卸载安装的软件包 $sudo cat cython/examples/setup_cython_call_cc_install_info.txt | xargs rm -rf
# 6. 模块维护者应该制作源码包；要实现可以运行 $python setup.py sdist
# 7. 如果源码发行包成功构建了，维护者也可以创建二进制发行包。依赖于平台，一个可用的命令如下
# $python setup.py bdist_wininst
# $python setup.py bdist_rpm
# $python setup.py bdist_dumb
