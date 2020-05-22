#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
from setuptools import setup

import lsclib


def get_file_content(filename):
    with open(filename, "r", encoding="UTF-8") as f:
        return f.read()


setup(
    name="litstrings-cli",
    version=lsclib.__version__,
    entry_points={"console_scripts": ["litstrings=lsclib.cmdline:main"]},
    description="A command line interface for LitStrings",
    long_description=get_file_content("README.md"),
    long_description_content_type="text/markdown",
    author="Iridium Intelligence",
    author_email="litstrings@iridiumintel.com",
    url="https://litstrings.info",
    license="GPLv2",
    dependency_links=[],
    setup_requires=[],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,<3.9",
    install_requires=get_file_content("requirements.txt").splitlines(),
    data_files=[],
    zip_safe=False,
    packages=["lsclib"],
    include_package_data=True,
    package_data={},
    keywords=("translation", "localization", "internationalization",),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
