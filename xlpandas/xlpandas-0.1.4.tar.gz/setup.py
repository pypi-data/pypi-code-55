#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    ld = f.read()

setup(
    name='xlpandas',
    version='0.1.4',
    description='Read and write xlsx/xlst using pandas/openpyxl while preserving Excel formatting',
    long_description=ld,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Francis Gassert',
    url='https://github.com/fgassert/xlpandas',
    packages=['xlpandas'],
    install_requires=['openpyxl','pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
