import codecs
import os
import sys
import re

from setuptools import find_packages, setup
from setuptools.command.install import install


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Build an absolute path from *parts* and and return the contents of the resulting file.

    Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_PATH = os.path.join("src", "dhm_module_base", "__init__.py")
META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


##############################################################################
NAME = "dhm_module_base"
VERSION = find_meta("version")  # Defined in src/PACKAGE/__init__.py

PACKAGES = find_packages(where="src")
PACKAGE_DIR = {"": "src"}
PACKAGE_DATA = {"dhm_module_base": ["configs/*",]}
KEYWORDS = ["eksempel"]
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/septima/dhm_module_base/issues",
    "Source Code": "https://github.com/septima/dhm_module_base",
}
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering :: GIS",
]

INSTALL_REQUIRES = [
    "click>=7.1",
    "click_plugins",
]

EXTRAS_REQUIRE = {"dev": ["pytest", "black"]}
ENTRY_POINTS = """
      [console_scripts]
      dhm_module_base=dhm_module_base.cli:cli
"""

###############################################################################


def readme():
    """Print long description."""
    with open("README.md") as desc:
        return desc.read()


class VerifyVersionCommand(install):
    """Command to check if Git Tag matches Package version."""

    description = "Verify that the git tag matches our version"

    def run(self):
        """Run VerifyVersionCommand."""
        # CircleCI release tag
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            # Check if sys.exit(info) is too intrusive
            sys.exit(info)


if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        description=find_meta("description"),
        long_description=readme(),
        long_description_content_type="text/markdown",
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        author=find_meta("author"),
        author_email=find_meta("email"),
        url=find_meta("uri"),
        license=find_meta("license"),
        packages=PACKAGES,
        package_dir=PACKAGE_DIR,
        include_package_data=True,
        package_data=PACKAGE_DATA,
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
        cmdclass={"verify": VerifyVersionCommand},
    )
