import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="textparsingtools",
    version="1.0.0",
    description="A collection of methods to read and organize data stored in text",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Reid Prichard",
    author_email="rprichard@liberty.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=['textparsingtools'],
    include_package_data=True,
    install_requires=["xlsxwriter"],
)