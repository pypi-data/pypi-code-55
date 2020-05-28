#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
    name='deepworm_algorithm',
    version='0.1',
    author='JohnsonNie',
    author_email='pubrcv@163.com',
    url='http://deepdiy.net/',
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
    setup_requires=[
        
    ],
    python_requires='>=3.6',
)
