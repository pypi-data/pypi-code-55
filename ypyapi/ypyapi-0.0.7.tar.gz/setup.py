#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists
from setuptools import setup
import ypyapi

setup(name="ypyapi",
      version=ypyapi.__VERSION__,
      description="A collection of tools for Python",
      long_description=(open('README.rst').read() if exists('README.rd') else ''),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
          "Operating System :: OS Independent",
          ],

      install_requires=[
          "selenium",
          ],

      author="PingyanYang",
      url="http://pypi.python.org/pypi/ypyapi",
      author_email="yangpingyan@gmail.com",
      license="MIT",
      packages=["ypyapi"])
