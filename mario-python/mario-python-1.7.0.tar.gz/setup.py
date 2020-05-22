#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages


with open('requirements/base.txt') as f:
    requirements = f.read().splitlines()


test_requirements = ['pytest']


setup(
    author="Mitchell Lisle",
    author_email='m.lisle90@gmail.com',
    description="A configurable data pipeline library.",
    install_requires=requirements,
    keywords='mario',
    name='mario-python',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={
        "mongo": ["pymongo==3.10.1"]
    },
    url='https://github.com/mitchelllisle/mario',
    version='1.7.0',
    zip_safe=False,
)
