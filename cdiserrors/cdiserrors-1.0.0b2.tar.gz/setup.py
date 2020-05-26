# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['cdiserrors']
install_requires = \
['cdislogging>=1.0.0,<2.0.0']

extras_require = \
{'flask': ['Flask>=1.1.2,<2.0.0']}

setup_kwargs = {
    'name': 'cdiserrors',
    'version': '1.0.0b2',
    'description': 'Gen3 shared exceptions and utilities.',
    'long_description': None,
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
