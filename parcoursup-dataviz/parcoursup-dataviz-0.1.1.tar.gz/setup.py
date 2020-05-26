# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parcoursup_dataviz']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'helium>=3.0.4,<4.0.0',
 'lxml>=4.5.1,<5.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pastel>=0.2.0,<0.3.0',
 'python-dotenv>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['parcoursup-dataviz = parcoursup_dataviz.cli:run']}

setup_kwargs = {
    'name': 'parcoursup-dataviz',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ewen Le Bihan',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
