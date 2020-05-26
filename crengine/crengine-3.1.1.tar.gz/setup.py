######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to LICENSE for further information
### File: setup.py
### Description: Packager script
### Last Modified: 26 May 2020
######################################################################

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crengine",
    version="3.1.1",

    package_data={
        "crengine": ["help/*.html"
                     ,"help/*.txt"
                     ,"CRE/demo/*.cre"
                     ,"CRE/library/readme.txt"
                     ,"CRE/methods/*.csv"
                     ,"CRE/towers/*.csv"
                     ,"CRE/towers/*/*.wav"]
        },

    author="Jonathan Wilson",
    author_email="stwilfridsbells@gmail.com",
    description="The Change Ringing Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://harrogatebellringers.org/bellview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
)

