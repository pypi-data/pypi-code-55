#!/usr/bin/env python3
"""
Setuptools configuration for VAIS ASR
"""

import os
import logging

from setuptools import setup


def read(fname):
    """
    Load content of the file with path relative to where setup.py is.

    Args:
        fname (str): file name (or path relative to the project root)

    Returns:
        str: file content
    """
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    retval = open(fpath).read()

    return retval


def read_list(fname):
    """
    Load content of the file and split it into a list of lines.

    Args:
        fname (str): file name (or path relative to the project root)

    Returns:
        List[str]: file content (one string per line) with end of lines
                   characters stripped off and empty lines filtered out
    """
    content = read(fname)
    retval = list(filter(None, content.split('\n')))

    return retval


def get_version(fname):
    """
    Retrieve version from the VERSION file.

    Args:
        fname (str): file containing only the version

    Returns:
        str: version with whitespace characters stripped off
    """
    return read(fname).strip()


logging.basicConfig(level=logging.INFO)

setup(
    name='vaisasr-python',
    version=os.getenv('VERSION', get_version('VERSION')),
    packages=['vaisasr'],
    url='https://github.com/vaisasr/vaisasr-python.git',
    license='MIT',
    author='VAIS',
    author_email='support@vais.vn',
    description='Python API client for VAIS ASR',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read_list('requirements.txt'),
    entry_points={
        'console_scripts': [
            'vaisasr = vaisasr.cli:main'
        ]
    },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio :: Speech"
    ],
    include_package_data=True,
)
