#!/usr/bin/env python
from setuptools import setup, find_packages
import re
import os


def get_version():
    fn = os.path.join(os.path.dirname(__file__), "rotating_free_proxies", "__init__.py")
    with open(fn) as f:
        return re.findall('__version__ = "([\d.\w]+)"', f.read())[0]


def get_long_description():
    readme = open("README.rst").read()
    changelog = open("CHANGES.rst").read()
    return "\n\n".join([readme, changelog.replace(":func:", "").replace(":ref:", "")])


setup(
    name="rotating-free-proxies",
    version=get_version(),
    author="Nabin Khadka",
    author_email="nbnkhadka14@gmail.com",
    license="MIT license",
    long_description=get_long_description(),
    description="Rotating proxies for Scrapy",
    url="https://github.com/nabinkhadka/rotating-free-proxies",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "attrs > 16.0.0",
        "six",
        "typing",
        "beautifulsoup4==4.8.2",
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Scrapy",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
