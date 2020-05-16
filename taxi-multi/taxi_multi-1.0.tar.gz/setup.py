#!/usr/bin/env python
from setuptools import find_packages, setup
from taxi_multi import __version__

install_requires = [
    'taxi>=5.0',
]

setup(
    name='taxi_multi',
    version=__version__,
    packages=find_packages(),
    description='Multi backend for Taxi',
    author='Alexandre Blin',
    author_email='alexandre@blin.fr',
    url='https://github.com/alexandreblin/taxi-multi',
    install_requires=install_requires,
    license='wtfpl',
    python_requires=">=3.6",
    entry_points={
        'taxi.backends': 'multi = taxi_multi.backend:MultiBackend'
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
