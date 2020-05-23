from setuptools import setup

setup(
  name = "subgal",
  version = "1.1.0",
  author = "John Baber-Lucero",
  author_email = "pypi@frundle.com",
  description = ("A collection of tools for creating html galleries from photos that have been sorted by sortphotos"),
  license = "GPLv3",
  url = "https://github.com/jbaber/subgal",
  packages = ['subgal'],
  install_requires = ['docopt', 'pillow', 'python-magic',],
  tests_require=['pytest'],
  entry_points = {
    'console_scripts': ['subgal=subgal.subgal:main'],
  }
)
