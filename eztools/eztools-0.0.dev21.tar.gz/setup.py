#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

with open('VERSION') as version_file:
    version = version_file.read()

requirements = [
    'requests',
    'assertpy',
    'arrow'
]

classifiers = ["License :: OSI Approved :: MIT License",
               "Topic :: Software Development",
               "Topic :: Utilities",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: MacOS :: MacOS X"] + \
              [("Programming Language :: Python :: %s" % x) for x in "3.5 3.6 3.7 3.8".split()]

setup(
    name='eztools',
    version=version,
    description="A handy module for Python programming, to make my life easier.",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Toby Qin",
    author_email='toby.qin@live.com',
    url='https://github.com/tobyqin/eztools',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={"eztools": ["data/*.*"]},
    install_requires=requirements,
    license="MIT license",
    keywords='eztools,handy,utils,utility',
    classifiers=classifiers,
    test_suite='tests',
    zip_safe=False
)
