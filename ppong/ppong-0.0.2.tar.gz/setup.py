#!/usr/bin/env python

"""
========
setup.py
========
Installs repo_name
DEV only:
git commit -am "version bump";git push origin master
git tag -a v$(python setup.py --version) -m "Update";git push --tags
"""
import sys
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from distutils.core import setup, find_packages, Extension

with open('requirements.txt') as f:
    required = f.read().splitlines()

# main setup
setup(
name='ppong',
author='Rohan Dandage',
author_email='rohanadandage@gmail.com',
version='0.0.2',
url='https://github.com/rraadd88/ppong',
download_url='https://github.com/rraadd88/ppong/archive/master.zip',
description='ppong project',
long_description='https://github.com/rraadd88/ppong',
#keywords=['','',''],
license='General Public License v. 3',
install_requires=required,
platforms='Tested on Ubuntu 16.04 64bit',
packages=find_packages(exclude=['test*', 'deps*', 'data*', 'data']),
entry_points={
    'console_scripts': ['ppong = ppong.run:parser.dispatch',],
    },
)
