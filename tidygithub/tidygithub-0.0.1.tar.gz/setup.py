#!/usr/bin/env python

import re
import ast
from setuptools import setup, find_namespace_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('tidygithub.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='tidygithub',
    version=version,
    py_modules=['tidygithub'],
    install_requires=[
        'numpy',
        'pandas',
        'plotnine',
        'PyGithub',
        ],
    description='tidy github API wrapping PyGithub',
    author='Michael Chow',
    author_email='mc_al_github@fastmail.com',
    url='https://github.com/machow/tidygithub'
    )
