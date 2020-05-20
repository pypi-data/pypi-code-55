# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stonks_trader',
 'stonks_trader.backtesting',
 'stonks_trader.cli',
 'stonks_trader.helpers',
 'stonks_trader.trade_strategies']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'numpy', 'pandas', 'pytse_client', 'requests', 'ta', 'typer']

setup_kwargs = {
    'name': 'stonks-trader',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
