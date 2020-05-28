#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup

version = '1.2.0'

setup(
    name='jutge-heartbeat',
    packages=['jutge.heartbeat'],
    install_requires=[
        'requests',
        'jutge-monitor',
    ],
    version=version,
    description='Heartbeat for worker machines of Jutge.org',
    long_description='Heartbeat for worker machines of Jutge.org',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-heartbeat',
    download_url='https://github.com/jutge-org/jutge-heartbeat/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'heartbeat'],
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
            'jutge-heartbeat=jutge.heartbeat:heartbeat.main',
            'jutge-heartbeat-listener=jutge.heartbeat:listener.main',
        ]
    }
)

# Steps to try new version:
# -------------------------
#
# pip3 uninstall --yes jutge-heartbeat
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
