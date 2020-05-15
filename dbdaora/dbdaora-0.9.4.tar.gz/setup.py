#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['dbdaora',
 'dbdaora.data_sources',
 'dbdaora.data_sources.fallback',
 'dbdaora.data_sources.memory',
 'dbdaora.hash',
 'dbdaora.hash.repositories',
 'dbdaora.service',
 'dbdaora.sorted_set',
 'dbdaora.sorted_set.repositories']

package_data = \
{'': ['*'],
 'dbdaora': ['_tests/*'],
 'dbdaora.hash': ['_tests/*', '_tests/datastore/*'],
 'dbdaora.hash.repositories': ['_tests/*'],
 'dbdaora.sorted_set': ['_tests/*', '_tests/datastore/*'],
 'dbdaora.sorted_set.repositories': ['_tests/*']}

install_requires = \
['circuitbreaker', 'cachetools', 'jsondaora']

extras_require = \
{'aioredis': ['aioredis'],
 'datastore': ['google-cloud-datastore'],
 'doc': ['mkdocs', 'mkdocs-material', 'markdown-include'],
 'test': ['black',
          'isort',
          'ipython',
          'mypy',
          'pytest-asyncio',
          'pytest-cov',
          'pytest-mock',
          'pytest']}

setup(name='dbdaora',
      version='0.9.4',
      description='Communicates with databases using repository pattern and service patterns',
      author='Diogo Dutra',
      author_email='diogodutradamata@gmail.com',
      url='https://github.com/dutradda/dbdaora',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.8',
     )
