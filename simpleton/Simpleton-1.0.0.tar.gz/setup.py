from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
name='Simpleton',
version='1.0.0',
description='Imports commonly used standard-library modules.',
long_description=long_description,
long_description_content_type="text/markdown",
url='https://github.com/c00lhawk607/simpleton',
author='Jordan Dixon',
author_email='jordandixon2004@outlook.com',
license='GNU General Public License v3 (GPLv3)',
packages=['simpleton'],
classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Natural Language :: English",
  "Topic :: Software Development :: Build Tools",
  "Topic :: Utilities"
],
zip_safe=True,
python_requires=">=3.0",
)