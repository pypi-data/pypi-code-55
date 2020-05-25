from setuptools import setup, find_packages
import os
from version_query import predict_version_str

file_dir = os.path.abspath(os.path.dirname(__file__))
__version__ = predict_version_str().split("+") [0]
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
    packages = find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 ',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.5',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/tillhainbach/' + name + '/issues',
        'Documentation': 'https://pyansiescapes.readthedocs.io/en/latest/',
        'Source': 'https://github.com/tillhainbach/' + name,
    },
)
