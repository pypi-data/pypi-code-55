import os
from setuptools import setup

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="flake8parser",
    description=(
        "A public python API for flake8 created by parsing the command line output."
    ),
    long_description=long_description,
    version="0.1.1",
    author="Alex M.",
    author_email="7845120+newAM@users.noreply.github.com",
    url="https://github.com/newAM/flake8parser",
    license="MIT",
    python_requires=">=3.6",
    install_requires=["flake8>=3.8.2"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["flake8parser"],
)
