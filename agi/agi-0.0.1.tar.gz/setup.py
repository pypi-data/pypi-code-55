import io
from setuptools import setup, find_packages
from agi.version import __version__

name = "agi"
author = "AGI itself"
license = "Apache-2.0"
description = (
    "Artificial General Intelligence with a convenient pip install"
)


def get_requirements():
    with io.open("requirements.txt") as f:
        return [
            line.strip()
            for line in f.readlines()
            if not line.strip().startswith("#")
        ]


setup(
    name=name,
    version=__version__,
    author=author,
    maintainer=author,
    description=description,
    long_description=io.open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    platforms=["Windows", "POSIX", "MacOSX"],
    license=license,
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
