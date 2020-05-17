#!/usr/bin/env python
"""The setup script."""
import os
import re
import sys

from setuptools import find_packages, setup


def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("pysolarenergy", "__version__.py")
    return re.search(regex, read(*path)).group("version")


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    name="pysolarenergy",
    version=get_version(),
    author="Hallen Maia",
    author_email="hallenmaia@me.com",
    description="Python module for SolarEnergy inverter",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hallenmaia/python-solarenergy",
    packages=find_packages(include=["pysolarenergy"]),
    test_suite="tests",
    install_requires=list(val.strip() for val in open("requirements.txt")),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: AsyncIO",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["api", "async", "client", "inverter", "solar"],
    license="MIT license",
)
