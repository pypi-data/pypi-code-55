"""
Setup pypi package for Datu SDK
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datu_sdk", # Replace with your own username
    version="0.0.1",
    author="Fisher Yu",
    author_email="f@datu.ai",
    description="SDK to use Datu service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datu-ai/datu-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"     
    ],
    python_requires='>=3.7',
)