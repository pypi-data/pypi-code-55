# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extractlib",
    packages=setuptools.find_packages(),
    version="0.0.3",
    author="Knoema",
    author_email="info@knoema.com",
    license="MIT",
    description="Python library which provides utilities for implementing custom extracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adaptivemgmt/extractlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3", "pytz", "requests", "pyyaml"]
)
