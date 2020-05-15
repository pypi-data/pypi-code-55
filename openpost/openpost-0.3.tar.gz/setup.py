#! /usr/bin/env python
#
# Copyright (C) 2020 Bob Swift
# <bswift@rsds.ca>

"""Builder for the 'openpost' package."""

import os
from setuptools import setup

DESCRIPTION = """A module to help prepare and execute html POST requests."""
DIST_NAME = "openpost"
# PKG_NAME = DIST_NAME + '-rdswift'   # use only for testing on https://test.pypi.org
PKG_NAME = DIST_NAME
AUTH_NAME = "Bob Swift"
AUTH_EMAIL = 'bswift@rsds.ca'
MAINT_NAME = AUTH_NAME
MAINT_EMAIL = AUTH_EMAIL
URL = "https://github.com/rdswift/OpenPost"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/rdswift/OpenPost"

with open("./README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("./openpost/__init__.py", "r") as f:
    LINES = f.readlines()
    for line in LINES:
        if line.startswith("__version__"):
            __version__ = line.split("= ")[-1].strip().strip('"')
            break

if __name__ == "__main__":
    if os.path.exists("MANIFEST.in"):
        os.remove("MANIFEST.in")

    setup(
        name=PKG_NAME,
        author=AUTH_NAME,
        author_email=AUTH_EMAIL,
        # maintainer=MAINT_NAME,
        # maintainer_email=MAINT_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        packages=["openpost"],
        version=__version__,
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=False,
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Internet :: WWW/HTTP",
        ],
        # python_requires='>=3.5',
        platforms="any",
        # package_data={},
        # scripts=[],
        # install_requires=[],
        # extras_require={},
    )
