# -*- coding: utf-8 -*-
import setuptools
from codecs import open  # To use a consistent encoding
from os import path
"""
name：项目的名称
version：项目的版本
author，author_email：作者和作者邮件
description：项目的简单介绍
long_description：项目的详细介绍
long_description_content_type：表示用哪种方式显示long_description，一般是 md 方式
url：项目的主页地址
packages：项目中包含的子包，find_packages() 是自动发现根目录中的所有的子包。
classifiers：其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。
"""
here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open("README.rst", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="chinaunicom",
    version="1.0.8",
    author="王若蒙",
    author_email="wangrm40@chinaunicom.cn",
    description="中国联通软件研究院专用python工具包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JustDoPython/justdopython.github.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)