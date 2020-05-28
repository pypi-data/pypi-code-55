#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nik

from setuptools import setup

# Read out version
version = nik.__version__

# Use README.md as long description for package
with open('README.md', 'r') as readme:
    long_description = readme.read()

requirements = []
# Read out requirements.txt
for path in ('requirements.txt',):
    with open(path, 'r') as f:
        lines = f.readlines()
        requirements.extend([line.strip() for line in lines if not line.startswith('#')])

setup(
    name = 'nik',
    version = version,
    author = 'Markus Beuckelmann',
    author_email = 'email@markus-beuckelmann.de',
    url = 'https://github.com/markus-beuckelmann/nik',
    download_url = f'https://github.com/markus-beuckelmann/nik/releases/download/{version}/nik-{version}.tar.gz',
    description = 'A simplistic, versatile companion to browse, navigate and visualize your text-based Zettelkasten.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = ['nik'],
    license='AGPLv3',
    entry_points = {
        'console_scripts': ['nik=nik.cli:nik'],
    },
    keywords = 'Zettelkasten nik markdown',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'License :: OSI Approved',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Education'
    ],
    include_package_data = True,
    install_requires = requirements,
    python_requires = '>=3.7'
)
