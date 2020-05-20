import os
from setuptools import find_packages, setup

from koco.about import __description__, __license__, __version__

REQ_FILE = 'requirements.txt'


def get_requires():
    reqpath = os.path.abspath(REQ_FILE)
    return [line.rstrip('\n') for line in open(reqpath)]


setup(
    name='koco',
    version=__version__,
    description=__description__,
    author='Jihyung Moon',
    author_email='mjihyung@gmail.com',
    url='https://github.com/inmoonlight/koco',
    license=__license__,
    packages=find_packages(),
    install_requires=get_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
    ],
    keywords='korean nlp datasets',
)
