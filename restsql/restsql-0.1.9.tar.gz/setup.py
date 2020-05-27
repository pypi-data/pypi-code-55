#! /usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='restsql',
    version='0.1.9',
    author="venzozhang",
    packages=setuptools.find_packages(),
    license='All right reserved',
    long_description="restsql",
    install_requires=[
        'certifi==2019.9.11',
        'chardet==3.0.4',
        'elasticsearch==5.4.0',
        'elasticsearch-dsl==5.3.0',
        'guppy==0.1.10',
        'idna==2.8',
        'ipaddress==1.0.23',
        'mysqlclient==1.4.2.post1',
        'numpy==1.16.5',
        'pandas==0.24.2',
        'psycopg2-binary==2.8.4',
        'pycrypto==2.6.1',
        'python-dateutil==2.8.0',
        'pytz==2019.2',
        'requests==2.22.0',
        'six==1.12.0',
        'urllib3==1.25.6',
        'peewee==3.13.2'
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)