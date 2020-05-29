# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


from setuptools import setup, find_packages


import raptorstr

setup(
    name="raptorstr",
    version=raptorstr.__version__,
    description="A package for working with strings with the purpose of generating code",
    long_description="""\
When generating code based off of format description files it is sometimes necessary
to conform strings to the code standard you are generating for. This lib is made for
this sole purpose and has some convenient functions for doing so with some thought out
decisions regarding where one is to break strings in different scenarios.
""",
    keywords="strings code case",
    packages=find_packages(),
    include_package_data=True,
    author="Andreas Stenberg",
    author_email="andreas@mewongu.com",
    url="https://github.com/Mewongu/raptorstr",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
)
