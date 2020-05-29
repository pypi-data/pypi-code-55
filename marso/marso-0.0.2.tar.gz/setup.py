#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup, find_packages

import marso


__AUTHOR__ = 'Yuan xy'
__AUTHOR_EMAIL__ = 'yuan_xin_yu@hotmail.com'

readme = open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read()

setup(name='marso',
      version=marso.__version__,
      description='A Move Parser',
      author=__AUTHOR__,
      author_email=__AUTHOR_EMAIL__,
      include_package_data=True,
      maintainer=__AUTHOR__,
      maintainer_email=__AUTHOR_EMAIL__,
      url='https://github.com/yuan-xy/marso',
      license='MIT',
      keywords='move/libra parser',
      long_description=readme,
      packages=find_packages(exclude=['test']),
      package_data={'marso': ['grammar/*.txt']},
      platforms=['any'],
      python_requires='>=3.7',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Editors :: Integrated Development Environments (IDE)',
          'Topic :: Utilities',
      ],
      extras_require={
          'testing': [
              'pytest>=3.0.7',
              'docopt',
          ],
      },
      )
