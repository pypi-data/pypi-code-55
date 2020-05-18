#!/usr/bin/env python3.7

# Python standard library imports
from pathlib import Path

# Non-standard library python package imports
from setuptools import (  # type: ignore
    find_packages,
    setup,
)

# Imports of module(s) internal to this project/package
from blackjack import version


setup(
    # Metadata
    name='x10-blackjack',
    version=version,
    author_email='x10an14@gmail.com',
    description='A small blackjack game.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/x10an14/blackjack',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
    ],

    # Package data
    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'click>=7,<8',
        'requests>=2,<3',
        # Hard-code tabulate's version due to being below v1.0.0
        'tabulate==0.8.7',
    ),
    entry_points='''
        [console_scripts]
        blackjack=blackjack.cli:cli
    ''',
    python_requires='>=3.7'
)
