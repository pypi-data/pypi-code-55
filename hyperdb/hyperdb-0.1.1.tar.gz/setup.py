from setuptools import setup, find_packages
import re
import os
import sys
import codecs

with open('requirements.txt') as f:
    required = f.read().splitlines()

try:
    # https://stackoverflow.com/questions/30700166/python-open-file-error
    with codecs.open("README.md", 'r', errors='ignore') as file:
        readme_contents = file.read()

except Exception as error:
    readme_contents = ""
    sys.stderr.write("Warning: Could not open README.md due %s\n" % error)


setup(name='hyperdb',
      version='0.1.1',
      description='Hyperdb provides wrapper functions for working with Tableau hyper datasources and moving data between Tableau Server, Google Cloud Platform and Microsoft Azure through a common interface',
      long_description=readme_contents,
      long_description_content_type="text/markdown",
      url='http://github.com/mhadi813/hyperdb',
      author='Muhammad Hadi',
      author_email='mhadi813@gmail.com',
      license='BSD',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Topic :: Office/Business",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      packages=find_packages(),
      install_requires=required,
      keywords="tableau hyper pandas google bigquery cloud storage azure sql database",
      zip_safe=False)
