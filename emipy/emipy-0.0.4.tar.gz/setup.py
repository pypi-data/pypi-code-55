# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:25:20 2020

@author: f-ove
"""


import setuptools
import os

with open ("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emipy",
    version="0.0.4",
    author="Flow2theryan",
    author_email="f.overberg@web.de",
    description="A small package for emission data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)






