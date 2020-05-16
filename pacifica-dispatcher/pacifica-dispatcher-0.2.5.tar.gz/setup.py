#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the pacifica service."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-dispatcher',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Dispatcher',
    url='https://github.com/pacifica/pacifica-dispatcher/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='Mark Borkum',
    author_email='mark.borkum@pnnl.gov',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    install_requires=[
        'celery',
        'cherrypy',
        'cloudevents-python',
        'jsonpath2',
        'pacifica-downloader',
        'pacifica-namespace',
        'pacifica-uploader',
        'peewee'
    ]
)
