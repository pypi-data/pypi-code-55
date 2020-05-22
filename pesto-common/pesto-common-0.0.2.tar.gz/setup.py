#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

requirements = []

setup(name='pesto-common',
      version='0.0.2',
      author='Dreampie',
      author_email='Dreampie@outlook.com',
      url='https://github.com/Dreampie/pesto',
      description='Minimalist python utils',
      keywords=['minimalist', 'python', 'utils', 'pesto'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      platforms=['all']
      )
