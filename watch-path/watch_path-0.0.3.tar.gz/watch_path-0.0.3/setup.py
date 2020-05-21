#!/usr/bin/env python3


from setuptools import (find_packages, setup)


with open(".github/README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "watch_path",
    version = "0.0.3",
    author = "S0AndS0",
    author_email = "StrangerThanBland@gmail.com",
    description = "Simple wrapper for `os.stat`, calls callback function time-stamp changes",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/python-utilities/watch_path",
    download_url = 'https://github.com/python-utilities/watch_path/archive/v0.0.3.tar.gz',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
    ],
)
