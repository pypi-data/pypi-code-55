#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ls2ncdu",
    version="0.0.2",
    author="Ming Chia/Kevin Murray",
    author_email="foss@kdmurray.id.au",
    description="NCDU crawler for systems where only ls is available",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    url="https://github.com/borevitzlab/ls2ncdu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[
        "ls2ncdu",
        "ls2find",
    ],
)
