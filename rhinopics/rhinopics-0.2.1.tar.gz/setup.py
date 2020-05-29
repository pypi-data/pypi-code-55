#! /usr/bin/env python
"""rhinopics setup file."""
import pathlib
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import versioneer

# The directory containing this file
HERE = pathlib.Path(__file__).parent

DESCRIPTION = 'Rhinopics, let the fat unicorn rename yours pics!'
LONG_DESCRIPTION = HERE.joinpath('README.md').read_text()

DISTNAME = 'rhinopics'
LICENSE = 'MIT'
AUTHOR = 'Axel Fahy'
EMAIL = 'axel@fahy.net'
URL = 'https://github.com/axelfahy/rhinopics'
DOWNLOAD_URL = ''
PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/axelfahy/rhinopics/issues',
    # 'Documentation': 'https://rhinopics.readthedocs.io/en/latest/',
    'Source Code': 'https://github.com/axelfahy/rhinopics'
}
REQUIRES = [
    'Click==7.0',
    'click-pathlib==2019.6.13.1',
    'exifread',
    'ffmpeg-python==0.2.0',
    'python-dateutil==2.8.0',
    'tqdm==4.32.1',
    'typing==3.6.6'
]
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Multimedia',
    'Topic :: Utilities']


class NoopTestCommand(TestCommand):
    def __init__(self, dist):
        print('Rhinopics does not support running tests with '
              '`python setup.py test`. Please run `make all`.')


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": NoopTestCommand})

setup(name=DISTNAME,
      maintainer=AUTHOR,
      version=versioneer.get_version(),
      packages=find_packages(exclude=('tests',)),
      maintainer_email=EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      cmdclass=cmdclass,
      url=URL,
      download_url=DOWNLOAD_URL,
      project_urls=PROJECT_URLS,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      classifiers=CLASSIFIERS,
      python_requires='>=3.6',
      install_requires=REQUIRES,
      entry_points={
          'console_scripts': [
              'rhinopics = rhinopics.__main__:main'
          ]
      },
      zip_safe=False)
