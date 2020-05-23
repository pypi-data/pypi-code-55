from os import path
from setuptools import find_packages, setup

VERSION = "0.1.0"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="verbose_ls",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=VERSION,
    description="Format 'ls' output into verbose, human readable output",
    url="https://github.com/NelsonScott/verbose_ls",
    packages=find_packages(),
    entry_points={"console_scripts": ["verbose_ls = verbose_ls:main"]},
    include_package_data=True,
    python_requires=">=3.7",
)
