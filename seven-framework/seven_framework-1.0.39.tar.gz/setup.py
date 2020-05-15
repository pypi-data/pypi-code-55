# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-22 21:25:59
@LastEditTime: 2020-05-15 21:22:01
@LastEditors: ChenXiaolei
@Description: 
"""
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="seven_framework",
    version="1.0.39",
    author="seven",
    author_email="tech@gao7.com",
    description="seven framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://gitlab.tdtech.gao7.com/python/seven_framework",
    packages=find_packages(),
    install_requires=[
        "elasticsearch <= 7.6.0",
        "requests <= 2.23.0",
        "PyMySQL <= 0.9.3",
        "python_dateutil <= 2.8.1",
        "redis <= 3.4.1",
        "pycryptodome <= 3.9.7",
        "tornado <= 6.0.4",
        "bleach <= 3.1.5",
        "pycket <= 0.3.0",
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='~=3.4',
)