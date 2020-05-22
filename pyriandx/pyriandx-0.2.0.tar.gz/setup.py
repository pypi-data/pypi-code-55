# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from pyriandx import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyriandx",
    version=__version__,
    author="UMCCR and Contributors",
    author_email="services@umccr.org",
    description="API client CLI/SDK for PierianDx web services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umccr/pyriandx",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    package_data={
        "pyriandx": ["json/*.json"]
    },
    entry_points={
        "console_scripts": ["pyriandx=pyriandx.cli:main"]
    },
    extras_require={
        "dev": [
            "pipdeptree",
            "sphinx",
            "twine",
            "setuptools",
            "wheel",
            "pdoc3",
        ],
        "test": [
            "pytest",
            "pytest-cov",
            "flake8",
            "mockito",
        ],
    },
    install_requires=[
        "requests",
        "docopt",
        "coloredlogs",
        "verboselogs",
        "colorama",
    ],
    python_requires=">=3.6",
)
