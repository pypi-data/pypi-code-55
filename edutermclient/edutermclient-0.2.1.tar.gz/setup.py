import os
from setuptools import setup, find_packages
import edutermclient

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = edutermclient.__name__,
    version = edutermclient.__version__,
    author = "Wim Muskee",
    author_email = "w.muskee@kennisnet.nl",
    description = ("Library for connecting to the Eduterm API"),
    license = "MIT",
    keywords = "eduterm client",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/kennisnet/py-eduterm-client",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires = [
         'requests'
         ]
)
