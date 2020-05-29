#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                                                           
# Copyright (C)2017 SenseDeal AI, Inc. All Rights Reserved  
#                                                           

"""                                                   
File: setup.py
Author: lzl
E-mail: zll@sensedeal.ai
Last modified: 2020/3/9
Description:                                              
"""

from setuptools import setup, find_packages
import sense_requests.config

setup(
    name='sense-requests-sdk',
    version=sense_requests.config.VERSION,
    packages=find_packages(),
    url='',
    license='BSD License',
    author='kafka0102',
    author_email='yujianjia@sensedeal.ai',
    description='Python SDK for Sense-Requests',
    long_description='',
    long_description_content_type="text/markdown",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'requests',
        'prettytable',
        'scrapy',
        'pymongo',
    ],
    entry_points={
        'console_scripts': [
            'sense_requests=sense_requests:main'
        ]
    }
)
