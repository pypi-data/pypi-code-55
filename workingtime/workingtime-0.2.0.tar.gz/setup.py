# encoding: utf-8

"""
# TODO description
"""

import os
import sys

from setuptools import setup, find_packages

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

DOCLINES = (__doc__ or '').split("\n")

with open(os.path.join(os.path.dirname(__file__),
                       'VERSION'), 'r') as version_file:
    version = version_file.read().strip()

setup(name='workingtime',
      version=version,
      description=DOCLINES[1],
      long_description="\n".join(DOCLINES[3:]),
      url='https://workingtime.readthedocs.io',
      maintainer='Pablo Manso',
      maintainer_email='92manso@gmail.com',
      include_package_data=True,
      platforms=['any'],
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.6, <4',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      install_requires=['numpy>=1.16', 'pandas'],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      test_suite='tests',
      zip_safe=False)
