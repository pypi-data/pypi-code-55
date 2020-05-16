#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'pyrdai',
    version = '1.0.2',
    install_requires=[
        'pymssql',
    ],
    packages=find_packages(),
    license = 'Apache License',
    author = 'Reshapedata',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'reshape data AI Services in py language ',
    keywords = ['reshapedata', 'rdai','pyrdai'],
    python_requires='>=3.6',
)
