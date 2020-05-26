from setuptools import setup, find_packages

setup(
    name="preapp",
    version="0.0.2",
    description="a tool that helps developers build github repositories from a design spec and backlog",
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(where="."),
    license="MIT",
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    package_data={"": ["*.yml", "*.js", "*.json"]},
    url="https://github.com/stephend017/preapp",
)
