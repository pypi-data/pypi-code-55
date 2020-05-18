# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/5/15 14:33
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ranking-metrics", #
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.1.1",
    license='MIT',
    author="Luke",
    author_email="nju.hyhb@gmail.com",
    description="ranking metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nju-luke/rank-metrics",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

    keywords=['ranking', 'ranking-metrics', 'ndcg', 'errs'],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],

)