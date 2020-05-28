#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
    name='deepworm_algorithm',
    version='0.1.3',
    author='JohnsonNie',
    author_email='pubrcv@163.com',
    url='http://www.deepdiy.net/',
    description='A set of algorithms for analysing worm image',
    packages=setuptools.find_packages(),
    install_requires=[
        'thinning-py3',
        'opencv-python',
        'matplotlib',
        'scikit-image',
        'networkx',
        'scipy',
        'numpy', 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
