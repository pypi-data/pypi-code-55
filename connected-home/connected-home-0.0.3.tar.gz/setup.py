# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'Flask>=1.1.2',
    'flask-socketio>=4.3.0',
    'flask-cors>=3.0.8',
    'gevent-websocket>=0.10.1'
]
test_requirements = [
]

setup(
    name="connected-home",
    version="0.0.3",
    description="A teaching environment simulating a connected home.",
    license="MIT",
    author="Data-Centric Design Lab <lab@datacentricdesign.org>",
    packages=find_packages(exclude=("tests",)),
    install_requires=requires,
    tests_require=test_requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
