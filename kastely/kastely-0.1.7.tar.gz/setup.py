# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kastely']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.1,<2.0',
 'ascii>=3.6,<4.0',
 'colorama>=0.4.3,<0.5.0',
 'pyfiglet>=0.8.0,<0.9.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['kastely = kastely.__main__:game']}

setup_kwargs = {
    'name': 'kastely',
    'version': '0.1.7',
    'description': '🏰 Race to the castle with this fun CLI Board Game!',
    'long_description': None,
    'author': 'Sam Poder',
    'author_email': 'hi@sampoder.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
