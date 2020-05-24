#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from setuptools import setup
import os
import re
from os import path

# def readme():
#     with open('README.md') as f:
#         return f.read()

cwd = os.getcwd()

def files_one_level(directory):
    f = os.popen('find '+ directory )
    l = []
    for line in f:
        fields = line.strip().split()
        l.append(fields[0])
    return l

def files_one_level_drop_pwd(directory):
    f = os.popen('find '+ directory)
    l = []
    for line in f:
        fields = line.strip().split()
        if not(os.path.isdir(fields[0])) and ("__init__.py" not in fields[0]):
            l.append(drop_pwd(fields[0]))
    return l

def drop_pwd(s):
    cwd = os.getcwd()
    result = ""
    if re.search(cwd, s):
        result = re.sub(cwd+'/', '', s)
    return result

# this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(name='damemysql',
      version='0.0.16',
      description='Learning about MYSQL from tests',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='sql mysql',
      url='http://github.com/davidam/damemysql',
      author='David Arroyo Menéndez',
      author_email='davidam@gnu.org',
      license='GPLv3',
      packages=['damemysql', 'damemysql.tests', 'damemysql.files'],
      package_dir={'damemysql': 'damemysql', 'damemysql.tests': 'damemysql/tests', 'damemysql.files': 'damemysql/files'},
      package_data={'damemysql': ['*'],
                    'damemysql.files': ['*'],
                    'damemysql.tests': ['*'],
                    'damemysql.root': ['*']},
      data_files=[('damemysql', ['README.org', 'README.md'] + files_one_level_drop_pwd(cwd+"/damemysql/files") + files_one_level_drop_pwd(cwd+"/damemysql/tests"))],
      install_requires=[
          'markdown',
          'MySQL-python'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
