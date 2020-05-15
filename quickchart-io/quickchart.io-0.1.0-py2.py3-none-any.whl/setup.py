# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickchart-python', 'quickchart-python.examples']

package_data = \
{'': ['*'],
 'quickchart-python': ['.git/*',
                       '.git/hooks/*',
                       '.git/info/*',
                       '.git/logs/*',
                       '.git/logs/refs/heads/*',
                       '.git/logs/refs/remotes/origin/*',
                       '.git/objects/06/*',
                       '.git/objects/0d/*',
                       '.git/objects/1b/*',
                       '.git/objects/1e/*',
                       '.git/objects/2f/*',
                       '.git/objects/47/*',
                       '.git/objects/4a/*',
                       '.git/objects/52/*',
                       '.git/objects/59/*',
                       '.git/objects/7b/*',
                       '.git/objects/7e/*',
                       '.git/objects/82/*',
                       '.git/objects/a5/*',
                       '.git/objects/ac/*',
                       '.git/objects/b4/*',
                       '.git/objects/ba/*',
                       '.git/objects/c2/*',
                       '.git/objects/e8/*',
                       '.git/objects/eb/*',
                       '.git/objects/f9/*',
                       '.git/objects/pack/*',
                       '.git/refs/heads/*',
                       '.git/refs/remotes/origin/*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'quickchart.io',
    'version': '0.1.0',
    'description': 'A client for quickchart.io, a service that generates static chart images',
    'long_description': None,
    'author': 'Ian Webster',
    'author_email': 'ianw_pypi@ianww.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
