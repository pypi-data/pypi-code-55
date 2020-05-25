import setuptools
import os
import sys
from setuptools.command.install import install

# dummyzarid version
VERSION = "0.0.4"

with open("README.md", "r") as fh:
    long_description = fh.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setuptools.setup(
    name="dummyzarid",
    version=VERSION,
    author="Teamgeek",
    author_email="support@teamgeek.io",
    description="Generate dummy South African ID numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamgeek-io/dummyzarid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests==2.23.0"],
    python_requires=">=3.6",
    cmdclass={"verify": VerifyVersionCommand},
)
