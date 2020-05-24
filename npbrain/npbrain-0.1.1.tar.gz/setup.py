import io
import os
import re

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# obtain version string from __init__.py
with open(os.path.join(here, 'npbrain', 'all.py'), 'r') as f:
    init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README and CHANGES
with io.open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    README = f.read()


setup(
    name='npbrain',
    version=version,
    description='NumpyBrain: A lightweight micro-core SNN simulation framework.',
    long_description=README,
    author='Chaoming Wang',
    author_email='oujago@hotmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15',
        'matplotlib',
        'numba',
    ],
    url='https://github.com/oujago/NumpyBrain',
)
