#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "ricksay"
DESCRIPTION = "Rick & Morty quotes of the day with ponies included!"
URL = "https://github.com/roma-guru/ricksay"
EMAIL = "voropaev.roma@gmail.com"
AUTHOR = "Roman Voropaev"
REQUIRES_PYTHON = ">=3.0.0"
VERSION = "0.2.2"

# What packages are required for this module to be executed?
REQUIRED = ["click==7.*"]

# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [("testpypi", "t", "Upload to TestPyPi instead")]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.testpypi = False

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        if not self.testpypi:
            os.system("twine upload dist/*")
        else:
            os.system("twine upload --repository testpypi dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")
        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude="png"),
    scripts=["scripts/ricksay"],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    package_data={"ricksay": ["balloons/*.say", "ponies/*/*.pony", "quotes/*.quotes"]},
    include_package_data=True,
    license="BSD",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Topic :: Games/Entertainment :: Fortune Cookies",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand,},
)
