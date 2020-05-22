#!/usr/bin/env python
# upload to pypi: python3 -m twine upload --repository testpypi dist

import codecs
import os.path

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))


def read(rel_path):
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
long_description = read(os.path.join(here, 'README.md'))

# Load requirements
with codecs.open(os.path.join(here, 'requirements.txt')) as f:
    requirements=[line.strip() for line in f.readlines()]

print(long_description)
setup(
    name="wmgraph",
    version=get_version("wmgraph/__init__.py"),
    author="Patrick Atamaniuk, wibas GmbH",
    author_email="patrick.atamaniuk@wibas.com",
    description="Microsoft Graph convenience library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/patrickatamaniuk/wmgraph",
    license="MIT License",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Office/Business",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
    ],
    keywords='Information Security,Microsoft,GraphAPI,graph api',

    packages=find_packages(),
    install_requires=requirements,
)
