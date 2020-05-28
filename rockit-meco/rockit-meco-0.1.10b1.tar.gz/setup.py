#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Optimal control problem."""

from setuptools import setup, find_packages
import glob
import os

version = "0.1.10b1"

data_files = [
  ('matlab/+rockit',glob.glob("matlab/+rockit/*.m")),
  ('examples',list(glob.glob("examples/*.m"))+list(glob.glob("examples/*.py"))),
  ('examples/helpers',list(glob.glob("examples/helpers/*.m"))+list(glob.glob("examples/helpers/*.py")))
]
for root, dir, files in os.walk("examples"):
  print(root,dir,files)

setup(
    name='rockit-meco',
    version=version,
    author="MECO-Group",
    author_email="joris.gillis@kuleuven.be",
    description="Rapid Optimal Control Kit",
    license='LICENSE',
    keywords="OCP optimal control casadi",
    url='https://gitlab.kuleuven.be/meco-software/rockit',
    packages=find_packages(exclude=['tests', 'examples']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'casadi>=3.5,<4.0',
        'numpy',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
    ],
    download_url='https://gitlab.kuleuven.be/meco-software/rockit/-/archive/v%s/rockit-v%s.tar.gz' % (version, version),
    data_files=data_files,
    include_package_data=True,
)
