#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['nondjango', 'nondjango.storages']

package_data = \
{'': ['*']}

install_requires = \
['boto3']

extras_require = \
{'test': ['pytest', 'pytest-cov']}

setup(name='nondjango-storages',
      version='0.3.2',
      description='nondjango-storages - Because the API is great but dependency on Django is not.',
      author='Alan Justino da Silva',
      author_email='alan.justino@yahoo.com.br',
      url='https://github.com/alanjds/nondjango-storages/',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.5',
     )
