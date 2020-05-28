#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md",'r') as f:
    long_description = f.read()

setup(name = "printcolor",
    version = "1.1.3",
    description = "print colorful string",
    author = "zack",
    author_email = "514838728@qq.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/dustingo/PrintColor.git",
    packages = find_packages(),
    install_requires = [],
    py_modules = ["printcolor","printcolor2"],
    platforms = ["linux"],
)
