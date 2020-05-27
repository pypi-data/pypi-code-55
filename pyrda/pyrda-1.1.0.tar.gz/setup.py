#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'pyrda',
    version = '1.1.0',
    install_requires=[
        'pymssql',
    ],
    packages=find_packages(),
    license = 'Apache License',
    author = 'Reshapedata',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'reshape data access in py language ',
    keywords = ['reshapedata', 'rda','pyrda'],
    python_requires='>=3.6',
)
