#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the proxy."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-proxy',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Proxy',
    url='https://github.com/pacifica/pacifica-uniqueid/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    entry_points={
        'console_scripts': [
            'pacifica-proxy=pacifica.proxy.__main__:main'
        ],
    },
    install_requires=[
        'cherrypy',
        'pacifica-namespace',
        'requests'
    ]
)
