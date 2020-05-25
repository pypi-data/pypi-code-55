#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import setuptools
import os


version = os.popen("git tag -l").read().split("\n")[0]
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='documentDownloader',
    version=version,
    author='OhYee',
    author_email='oyohyee@oyohyee.com',
    url='https://github.com/OhYee/documentDownloader',
    description=u'book118文档下载器',
    packages=setuptools.find_packages(),
    install_requires=['Pillow', 'reportlab', 'requests'],
    entry_points={
        'console_scripts': [
            'documentDownloader=book118:main',
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
