from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name = "MMC_demo",
    version = "0.3",
    packages = find_packages(),
    description = 'MicroMOOC demo test',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'MicroMOOC',
    author_email = 'support@micromooc.com',
    url = 'https://micromooc.com/',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)