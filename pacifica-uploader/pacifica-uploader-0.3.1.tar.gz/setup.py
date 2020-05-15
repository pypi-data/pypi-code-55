#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the metadata."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-uploader',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Uploader',
    url='https://github.com/pacifica/pacifica-python-uploader/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    install_requires=['requests']
)
