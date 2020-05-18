#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="ypyapi",
      version="0.0.3",
      description="A collection of tools for Python",
      long_description=long_description,
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
