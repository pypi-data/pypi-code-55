#!/usr/bin/env python

import os
import setuptools

__version__ = '1.15'


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name = 'git-remote-cvm',
    packages = ['git_remote_cvm'],
    version = __version__,
    description = 'Git remote prefix to simplify pushing to and pulling from CodeCommit using the CVM.',
    long_description = read('README.rst'),
    author = 'Amazon Web Services and Jeremy Axmacher',
    url = 'https://github.com/jcaxmacher/git-remote-cvm',
    license = 'Apache License 2.0',
    install_requires = ['botocore >= 1.10.4'],
    entry_points = {
        'console_scripts': [
            'git-remote-cvm = git_remote_cvm:main',
        ],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)
