#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="taste",
    version="0.0.0",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Peter Badida",
    author_email="keyweeusr@gmail.com",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Jupyter",
        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    install_requires=["ensure"],
    extras_require={"release": ["setuptools", "twine"]},
    python_requires=">=3.6"
)
