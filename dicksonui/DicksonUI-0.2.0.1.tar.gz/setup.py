#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#  
from setuptools import setup
import os
# The directory containing this file
package_dir = os.path.dirname(__file__)

# The text of the README file
README = open(package_dir + "README.md").read()

# This call to setup() does all the work
setup(
    name="DicksonUI",
    version="0.2.0.1",
    description="Lightweight And Full Featured Browser Based UI/GUI(Graphical User Interface Library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ksengine/DicksonUI",
    author="KavinduSanthusa",
    author_email="kavindusanthusa@rgmail.com",
    keywords="lightweight  full featured browser based ui gui user\
interface graphical user interface library powerful",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dicksonui"],
    include_package_data=True,
)
