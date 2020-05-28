# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
        {'encoders': 'lib/image-encoders/src/encoders', 'texturize': 'src/texturize'}

packages = \
['encoders', 'texturize']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'progressbar2>=3.51.3,<4.0.0']

entry_points = \
{'console_scripts': ['texturize = texturize.__main__:main']}

setup_kwargs = {
    'name': 'texturize',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Alex J. Champandard',
    'author_email': '445208+alexjc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
