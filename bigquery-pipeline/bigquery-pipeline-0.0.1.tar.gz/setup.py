#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='bigquery-pipeline',
    version='0.0.1',
    author='Antoine Delorme',
    author_email='antoine.delorme@gmail.com',
    packages=find_packages(),
    install_requires=[
        'google-cloud-core>=1.0.0',
        'tensorflow-metadata==0.14.0',
        'tensorflow-transform==0.14.0',
    ],
)
