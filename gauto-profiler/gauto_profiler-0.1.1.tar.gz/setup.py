#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: qintianchen
# Mail: 1365265750@qq.com
# Created Time: 2020-5-15 11:44:00
#############################################


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="gauto_profiler",
    version="0.1.1",
    author="qintianchen",
    author_email="1365265750@qq.com",
    description="A tool for game automation on android platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/qintianchen/AndroidGameProfiler.git",
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.4',
)