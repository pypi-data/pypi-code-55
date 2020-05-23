from setuptools import setup
import os


NAME = 'annotyped'
DESCRIPTION = 'A lightweight library for type checking and type casting annotated vars.'
URL = 'https://gitlab.com/sj1k/annotyped'
EMAIL = '42Echo6Alpha@gmail.com'
AUTHOR = 'Steven "sj1k" Core'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '0.1.2'

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    packages=['annotyped'],
)
