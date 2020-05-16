#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from pathlib import Path
from setuptools import find_packages, setup

#package meta-data.
NAME = 'solar_prod_suvilahti_ml_model'
DESCRIPTION = 'Study project. A regression model to predict Solar Energy Production.'
URL = 'https://github.com/screwdriver66/solar_prod_suvilahti'
EMAIL = 'simo.uimonen@gmail.com'
AUTHOR = 'Semen Uimonen'
REQUIRES_PYTHON = '>=3.6.0'

#package requirements
def list_reqs(filename='requirements.txt'):
    with open(filename) as f:
        return f.read().splitlines()

# CHECK LICENSE AND TROVE CLASSIFIERS!!!!
here = os.path.abspath(os.path.dirname(__file__))
#As a README for a long discription:
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# load the package __version__.py module as a dictionary
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / 'regression_model'
about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version

VERSION = _version

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'regression_model': ['VERSION']},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

)
