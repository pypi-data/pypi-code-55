# -*- coding: utf-8 -*-

import setuptools

setuptools._install_setup_requires({'setup_requires': ['git-versiointi']})
from versiointi import asennustiedot

setuptools.setup(
  name='python-mmaare',
  description='Python-moduulimääretoteutus',
  url='https://github.com/an7oine/python-mmaare.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  py_modules=['mmaare'],
  **asennustiedot(__file__),
)
