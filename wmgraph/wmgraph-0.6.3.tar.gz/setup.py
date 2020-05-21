#!/usr/bin/env python
# upload to pypi: python3 -m twine upload --repository testpypi dist

import codecs
import os.path

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="wmgraph",
    version=get_version("wmgraph/__init__.py"),
    author="Patrick Atamaniuk, wibas GmbH",
    author_email="patrick.atamaniuk@wibas.com",
    description="Microsoft Graph base library",
    long_description="""Microsoft Graph base library

    api and utility methods to use MS Graph functionality
    """,
    url="https://www.wibas.com/",
    license="MIT",
    packages=find_packages(),
    # scripts = ["wmssync"],
    entry_points={
        'console_scripts': ['wmssync=wmssync.cli:main']
    },
    install_requires=[
        "requests>=2,<3",
        "msal>=0,<2",
        "quickxorhash",
    ],
)
