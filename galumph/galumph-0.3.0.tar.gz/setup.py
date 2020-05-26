#!/usr/bin/env python

# SPDX-FileCopyrightText: 2016-2017 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import os.path

from setuptools import setup


def read(filename):
    repo_dir = os.path.dirname(__file__)
    full_path = os.path.join(repo_dir, filename)
    with open(full_path, 'r') as f:
        return f.read()


setup(
    name='galumph',
    version='0.3.0',
    description='Calculate ALM using GPU acceleration',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://git.embl.de/grp-svergun/galumph',
    author='Christopher Kerr',
    author_email='chris.kerr@mykolab.ch',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.5',
    requires=["pyopencl"],
    packages=[
        'galumph',
    ],
    package_dir={'galumph': 'src/python'},
    package_data={
        'galumph': ["cl-src/*.cl"],
    },
)
