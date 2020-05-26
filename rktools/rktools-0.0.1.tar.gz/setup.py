################
## setup.py   ##
################

# check with:
# (base)$ python setup.py check

import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The text of the version.txt file
VERSION = (HERE / "version.txt" ).read_text()

# if format is version=x.y.z (e.g. for bumpversion)
if VERSION.find("=") -1:
    VERSION = VERSION.split("=")[1].strip()

setup(

    # meta

    name = "rktools", # the pip name
    version = VERSION,
    description = "The Régis Kla Python tools library",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/rejux/rktools-lib",
    author = "Régis Kla",
    author_email = "klaregis@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

    # body

    zip_safe = False,
    packages = find_packages(exclude=["contrib", "docs", "tests"]),
    include_package_data=True,

    # DO THIS IN PARALLEL OF MANIFEST.in
    # package_dir={
    #    "rktools": "rktools",
    #    "rktools.tests": "rktools/tests"
    #},

    # Requirements

    # python_requires = "=3.0.*, <4",
    
    install_requires=["tqdm"]

)
