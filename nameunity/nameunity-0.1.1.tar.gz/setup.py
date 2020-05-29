#!/usr/bin/env python
#
# Author: LucasD11 <yuanzhendai@gmail.com>
#
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nameunity",
    version="0.1.1",
    author="LucasD11",
    author_email="yuanzhendai@gmail.com",
    description="A simple tool to help you unity file names.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasd11/nameunity",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['nameunity=nameunity.main:main'],
    }
)
