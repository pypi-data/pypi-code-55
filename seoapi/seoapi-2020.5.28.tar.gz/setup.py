#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re

package = "seoapi"

with open("README.md", "r", encoding="utf8") as fh:
    readme = fh.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


setup(
    name="seoapi",
    version=get_version(package),
    description="Библиотека для сервиса seoapi.ru",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["seoapi"],
    install_requires=["requests"],
    license="MIT",
    url="https://github.com/pavelmaksimov/seoapi-lib",
    author="Pavel Maksimov",
    keywords="python,seo,api,seoapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
