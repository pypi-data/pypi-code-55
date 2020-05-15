#-------------------------------------------------------------------------------
# Name:        setup.py
# Purpose:
#
# Author:      moham
#
# Created:     15-05-2020
# Copyright:   (c) moham 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from setuptools import setup,find_packages
fh = open("C:\\pyth\\README.md", "r")
long_description = fh.read()

setup(
    name="Tmfiles", # Replace with your own username
    version="0.1",
    author="Dr.tamer",
    author_email="tmrbe2006@Gmail.com",
    description="Files Treat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    keywords="Files",
    scripts=["Tmfiles.py"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)









def main():
    pass

if __name__ == '__main__':
    main()
