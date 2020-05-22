#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

requirements = ['pesto-common==0.0.1']

setup(name='pesto-orm',
      version='0.0.2',
      author='Dreampie',
      author_email='Dreampie@outlook.com',
      url='https://github.com/Dreampie/pesto',
      description='Minimalist python-orm framework',
      keywords=['minimalist', 'python', 'mysql', 'orm', 'pesto'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      platforms=['all']
      )
