#!/usr/bin/env python
# coding: utf-8

from os import path as os_path
from setuptools import setup


__version__ = "1.0.1"
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='ctype_struct',  # 包名
    python_requires='>=3.7.0', # python环境
    version=__version__, # 包的版本
    description="python解析C结构体16进制数据.",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="songchuhua", # 作者相关信息
    author_email='sch15625785335@163.com',
    url='https://github.com/TesterSong/Ctype-Struct-Python.git',
    # 指定包信息，还可以用find_packages()函数
    packages=[
        'ctype_struct',
    ],
    include_package_data=True,
    license="MIT",
    keywords=['C struct'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)