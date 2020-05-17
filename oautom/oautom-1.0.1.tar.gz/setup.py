#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='oautom',
    version='1.0.1',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/FabienArcellier/oautom",
    install_requires = [
        'apscheduler'
    ],
    extras_require={
        'dev': [
            'pylint',
            'coverage',
            'flask',
            'twine'
        ]
    },
    classifier= [
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: POSIX :: Linux'
    ],
)
