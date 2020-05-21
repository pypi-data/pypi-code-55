import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = "regression_model_module",
    version = "0.0.1",
    author = "Sharabh Shukla",
    author_email = "andrewjcarter@gmail.com",
    description = ("An demonstration of how to create, document, and publish a python package"),
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    license = "MIT",
    keywords = "core package",
    url = "https://sharabhshukla@git.fury.io/sharabhshukla/housepricemodel.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy >= 1.15.0",
    "joblib >= 0.14.1",
    "catboost >= 0.21",
    "pandas >= 0.25.0",
    "scikit-learn <= 0.23.0",
    "feature-engine >= 0.4.0",
    "ipykernel>=4.1",
    "tornado>=5.0",
    "loguru" ],
    include_package_data=True,
    zip_safe=False,
)