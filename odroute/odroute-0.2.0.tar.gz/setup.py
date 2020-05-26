# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

INSTALL_REQUIREMENTS = [
    "pyzmq>=16.0",
    "PyYAML<5.2 ; python_version <= '3.4'",
    "PyYAML ; python_version >= '3.5'"
]

setup(
    author='Jonas Ohrstrom',
    author_email='ohrstrom@gmail.com',
    url='https://github.com/digris/odr-stream-router',
    name='odroute',
    version='0.2.0',
    description='A tool to route streams from ODR-AudioEnc',
    packages=find_packages(),
    install_requires=INSTALL_REQUIREMENTS,
    entry_points='''
        [console_scripts]
        odroute=odroute:cli.main
    ''',
)
