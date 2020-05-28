#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.0"

def readme():
    """ print long description """
    with open('README.md') as f:
        long_descrip = f.read()
    return long_descrip
    
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CI_COMMIT_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="stravatool",
    version=VERSION,
    description="A tool to help with strava's api.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rveach/stravatool/",
    author="Ryan Veach",
    author_email="rveach@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
    ],
    keywords=['Strava', 'API'],
    packages=['stravatool'],
    install_requires=[
        'requests>=2.20.0',
    ],
    python_requires='>=3.5',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    scripts=['scripts/stravatool-helper.py'],
)
