#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup

version = '1.1.0'

setup(
    name='jutge-util',
    packages=['jutge.util'],
    install_requires=[
        'pyyaml',
    ],
    version=version,
    description='Common utilities for Jutge.org\'s scripts',
    long_description='Common utilities for Jutge.org\'s scripts',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-util',
    download_url='https://github.com/jutge-org/jutge-util/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'util'],
    license='Apache',
    zip_safe=False,
    include_package_data=True,
    setup_requires=['setuptools'],
)

# Steps to try new version:
# -------------------------
#
# pip3 uninstall --yes jutge-util
# pip3 install .

# Steps to distribute new version:
# --------------------------------
#
# increment version in the top of this file
# git commit -a
# git push
# git tag 1.1.1 -m 'Release 1.1.1'
# git push --tags origin master
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
#
# More docs:
# http://peterdowns.com/posts/first-time-with-pypi.html
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
