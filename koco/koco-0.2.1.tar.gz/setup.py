import os
from setuptools import find_packages, setup

REQ_FILE = 'requirements.txt'
VERSION = '0.2.1'


def get_requires():
    thisdir = os.path.dirname(__file__)
    reqpath = os.path.join(thisdir, REQ_FILE)
    return [line.rstrip('\n') for line in open(reqpath)]


def long_description():
    return """# koco

    `koco` is a library to easily access [`kocohub`](https://github.com/kocohub) datasets. <br>
    `kocohub` contains **KO** rean **CO** rpus for natural language processing.

    ## Usage
    Using `koco` is similar to [`nlp`](https://github.com/huggingface/nlp). The main methods are:
    - `koco.list_datasets()`: list all available datasets and their modes in [`kocohub`](https://github.com/kocohub)
    - `koco.load_dataset(dataset_name, mode)`: load dataset in [`kocohub`](https://github.com/kocohub) with data-specific mode
    """


setup(
    name='koco',
    version=VERSION,
    description='A library to easily access kocohub datasets',
    long_description=long_description(),
    author='Jihyung Moon',
    author_email='mjihyung@gmail.com',
    url='https://github.com/inmoonlight/koco',
    license='MIT',
    packages=find_packages(),
    install_requires=get_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
    ],
    keywords='korean nlp datasets',
)
