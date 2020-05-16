from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="openblu",
    version="1.0",
    author="Intellivoid Technologies",
    author_email="nocturn9x@intellivoid.net",
    description="Official Python 3 wrapper around the OpenBlu API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intellivoid/OpenBlu-Python-Wrapper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='>=3.6',
)
