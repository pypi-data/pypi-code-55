from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="preapp",
    version="0.0.3",
    description="a tool that helps developers build github repositories from a design spec and backlog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(where="."),
    license="MIT",
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    package_data={"": ["*.yml", "*.js", "*.json"]},
    url="https://github.com/stephend017/preapp",
    python_requires=">=3.6",
)
