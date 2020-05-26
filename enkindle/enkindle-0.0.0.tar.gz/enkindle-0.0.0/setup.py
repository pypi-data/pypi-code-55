from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="enkindle",
    version="0.0.0",
    author="Thomas Johansen",
    author_email="thomasjo@gmail.com",
    description="A lightweight wrapper for Ignite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasjo/enkindle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    python_requires=">=3.8",
)
