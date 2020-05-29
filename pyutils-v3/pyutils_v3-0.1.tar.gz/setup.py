#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutils_v3",
    version="0.1",
    author="Lam Nguyen",
    author_email="lamfm95@gmail.com",
    description="A handy library inspired by kaldi/egs/wsj/utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamnguyen95/pyutils_v3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
    ]
)
