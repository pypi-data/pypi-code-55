from setuptools import setup, find_packages

setup(
    name='bifrostapi',
    version='0.0.9',
    description='Datahandling functions for bifrost dashboard',
    url='https://github.com/ssi-dk/bifrostapi',
    author="Martin Basterrechea",
    author_email="mbas@ssi.dk",
    packages=find_packages(),
    install_requires=['pymongo'],
    python_requires='>=3.6'
    )
