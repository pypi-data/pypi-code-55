from setuptools import setup, find_packages
import os
from version_query import query_version_str

file_dir = os.path.abspath(os.path.dirname(__file__))
__version__ = query_version_str() + "1"
name = 'pyansiescapes'

# Get the long description from the README file
with open(os.path.join(file_dir, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = name,
    version = __version__,
    author='Till Hainbach',
    author_email='Till.Hainbach@posteo.de',
    description = 'Python package for quick and readable console manipulation using ANSI Escapes Sequences',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tillhainbach/' + name,
    packages = find_packages(name),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 ',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.5',
)
