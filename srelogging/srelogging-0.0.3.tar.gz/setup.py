"""setup.py

Used for installing srelogging via pip.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(install_requires=["pyyaml"],
      name="srelogging",
      version="0.0.3",
      description="Common logging functions for SRE python scripts.",
      long_description=repo_file_as_string("README.md"),
      long_description_content_type="text/markdown",
      author="Figglewatts",
      classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: System :: Logging"
      ],
      keywords="sre logging",
      author_email="sgibson@glasswallsolutions.com",
      py_modules=['srelogging'],
      python_requires=">=3.6")
