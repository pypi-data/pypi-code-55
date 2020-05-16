import os
from setuptools import setup, find_packages

NAME = "consistentor"
DESCRIPTION = "Consistentor helps you select things consistently"
URL = "https://github.com/jannekem/consistentor"
AUTHOR = "Janne Kemppainen"
VERSION = os.environ.get("VERSION", "0.0.1")
PYTHON_VERSION = ">=3.6.0"
LICENSE = "MIT"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
]

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read()

with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    version=VERSION,
    packages=find_packages(),
    url=URL,
    author=AUTHOR,
    install_requires=REQUIREMENTS,
    python_requires=PYTHON_VERSION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    classifiers=CLASSIFIERS,
)
