#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ttcal - calendar operations
===========================
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.6
Topic :: Software Development :: Libraries
"""

import sys, os
import setuptools

version = '1.0.7'

DIRNAME = os.path.dirname(__file__)
description = open(os.path.join(DIRNAME, 'README.rst'), 'r').read()


setuptools.setup(
    name='ttcal',
    version=version,
    url='https://github.com/datakortet/ttcal',
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    requires=[],
    install_requires=[
        'six',
        'future',
    ],
    # description=__doc__.strip(),
    long_description=description,
    classifiers=[line for line in classifiers.split('\n') if line],
    packages=setuptools.find_packages(exclude=['tests']),
    zip_safe=False,
)
