#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, isfile
from os import walk
import re
from setuptools import setup, find_packages

version_file = os.path.abspath(os.path.join('django_npick', '__init__.py'))
with open(version_file) as f:
    data = f.readline().strip()
version = re.findall("'(.*?)'", data)[0]

with open("README.md", "r") as fh:
    long_description = fh.read()


def package_files(directories):
    '''find static files'''
    paths = []
    for item in directories:
        if isfile(item):
            paths.append(join('..', item))
            continue
        for (path, directories, filenames) in walk(item):
            for filename in filenames:
                paths.append(join('..', path, filename))
    return paths


setup(
    name='django-npick',
    version=version,
    author='Mikele',
    author_email='blive200@gmail.com',
    license='BSD',
    description='Django Pick material Icon Widget',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/toyourheart163/django-npick',
    packages=find_packages(),
    package_data={
        '': package_files([
            'django_npick/static',
            'django_npick/templates'
        ])
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
