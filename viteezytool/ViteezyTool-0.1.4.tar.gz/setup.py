# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viteezytool', 'viteezytool.data', 'viteezytool.processor']

package_data = \
{'': ['*'],
 'viteezytool': ['resources/*',
                 'resources/img/*',
                 'resources/word_templates/*']}

install_requires = \
['docxtpl>=0.9.2,<0.10.0', 'pandas>=1.0.3,<2.0.0', 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['vit-tool = viteezytool.app:run']}

setup_kwargs = {
    'name': 'viteezytool',
    'version': '0.1.4',
    'description': 'Custom tool for Viteezy to generate customized word documents from an excel database',
    'long_description': None,
    'author': 'sander',
    'author_email': 'sander@rolisa.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
