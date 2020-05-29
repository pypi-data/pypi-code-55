#!/usr/bin/env python
from codecs import open

from setuptools import setup


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


classifiers = [
    # Pick your license as you wish (should match "license" above)
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
setup(
    name="dataschemas",
    version="0.0.0",
    description="Flexible object serialization and validation, built on JSON Schema",
    author="Robert Singer",
    author_email="robertgsinger@gmail.com",
    packages=["dataschemas"],
    url="https://github.com/rsinger86/dataschemas",
    license="MIT",
    keywords="schema validation jsonschema serialization deserialization specification",
    long_description=readme(),
    classifiers=classifiers,
    long_description_content_type="text/markdown",
)
