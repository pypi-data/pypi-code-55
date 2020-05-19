#!/usr/bin/env python3
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dev-container",
    version="0.1",
    author="Marcel Hollerbach",
    author_email="mail@bu5hm4n.de",
    description="A small bin tool that will spin up a docker for you. The docker will be picked from your CI tools, and can be used instead of the host system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcelhollerbach/dev-container",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="Apache 2.0",
    scripts=['dev-container'],
    install_requires=['pyyaml']
)
