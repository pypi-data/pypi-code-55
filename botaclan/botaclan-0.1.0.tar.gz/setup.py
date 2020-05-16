# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botaclan', 'botaclan.cogs', 'botaclan.google', 'botaclan.helpers']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=14.0,<15.0',
 'dateparser>=0.7.4,<0.8.0',
 'discord.py>=1.3.3,<2.0.0',
 'google-api-python-client>=1.8.3,<2.0.0',
 'google-auth-httplib2>=0.0.3,<0.0.4',
 'google-auth-oauthlib>=0.4.1,<0.5.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'sentry-sdk>=0.14.4,<0.15.0',
 'vyper-config>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['botaclan = botaclan.__main__']}

setup_kwargs = {
    'name': 'botaclan',
    'version': '0.1.0',
    'description': "Bataclan's official bot",
    'long_description': "# botaclan\nBataclan's official bot\n",
    'author': 'Gabriel Tiossi',
    'author_email': 'gabrieltiossi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bataclanofficial/botaclan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
