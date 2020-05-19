#!/usr/bin/env python
import os
import sys
from codecs import open
from setuptools import setup
from ddc import info

if sys.version_info < (3, 6, 0):
    print("Python 3.6+ is required")
    exit(1)

here = os.path.abspath(os.path.dirname(__file__))

DEPENDENCIES = ["requests>=2.19.1"]

setup(
    name=info.__package_name__,
    version=info.__version__,
    entry_points={
        'console_scripts': ['ddc=ddc.cli:main'],
    },
    description="Devision Developers Cli",
    long_description="",
    url="https://github.com/devision-io/ddc",
    author="Devision",
    author_email="info@devision.io",
    license="Apache 2.0",
    zip_safe=False,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=DEPENDENCIES,
    python_requires=">=3.6",
    packages=["ddc"],
    package_data={"": ["LICENSE"]},
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
)
