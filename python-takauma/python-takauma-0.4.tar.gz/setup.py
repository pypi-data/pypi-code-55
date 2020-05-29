# -*- coding: utf-8 -*-

import setuptools

setuptools._install_setup_requires({'setup_requires': ['git-versiointi']})
from versiointi import asennustiedot

setuptools.setup(
  name='python-takauma',
  description='Python-moduulien tiedostoversiointi',
  url='https://github.com/an7oine/python-takauma.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  packages=setuptools.find_packages(),
  include_package_data=True,
  zip_safe=False,
  extras_require={
    'kehitys': ['git-versiointi>=1.4.4'],
  },
  **asennustiedot(__file__),
)
