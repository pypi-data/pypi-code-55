# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysapphire']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysapphire',
    'version': '0.1.1',
    'description': 'Python implementation of the Sapphire II Stream Cipher Algorithm',
    'long_description': "# pysapphire\n\npysapphire is a python port of the Sapphire II stream cipher based on implementations found in CrossWire's [SWORD](http://www2.crosswire.org/sword/index.jsp) and [JSword](https://www.crosswire.org/jsword/), which are in turn based on a specification written by Michael Paul Johnson in 1995 and released to the public domain.",
    'author': 'Jasper Chan',
    'author_email': 'jasperchan515@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gigahawk/pysapphire',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
