#!/usr/bin/env python3
# coding=utf-8

import os
from setuptools import setup
from glob import glob


version = '1.0.0'


setup(
    name='jutge-monitor',
    packages=['jutge.monitor'],
    install_requires=['pyyaml>=5.1', 'uptime', 'psutil', 'py-cpuinfo', 'jsons'],
    version=version,
    description='Monitor for worker machines of Jutge.org',
    long_description='Monitor for worker machines of Jutge.org',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-monitor',
    download_url='https://github.com/jutge-org/jutge-monitor/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'monitor'],
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
    ],
    zip_safe=False,
    include_package_data=True,
    setup_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'jutge-monitor=jutge.monitor:monitor.main',
        ]
    }
)


# Steps to try new version:
# -------------------------
#
# pip3 uninstall --yes jutge-monitor
# pip3 install .

# Steps to distribute new version:
# --------------------------------
#
# increment version in the top of this file
# git commit -a
# git push
# git tag 1.1.1 -m "Release 1.1.1"
# git push --tags origin master
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
#
# More docs:
# http://peterdowns.com/posts/first-time-with-pypi.html
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
#
# new: use upload.sh