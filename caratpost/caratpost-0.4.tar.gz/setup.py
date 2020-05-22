from setuptools import setup

import os
import re

__version__ = '0.4'

setup(
    name='caratpost',
    version=__version__,
    packages=[
        'caratpost',
    ],
    author='Thomas Oberbichler',
    author_email='thomas.oberbichler@tum.de',
    install_requires=[
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'carat-post=caratpost.main:main'
        ]
    }
)
