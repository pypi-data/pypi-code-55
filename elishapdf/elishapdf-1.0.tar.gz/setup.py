import setuptools

from pathlib import Path

setuptools.setup(
    name="elishapdf",
    version="1.0",
    longdescription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])

)
