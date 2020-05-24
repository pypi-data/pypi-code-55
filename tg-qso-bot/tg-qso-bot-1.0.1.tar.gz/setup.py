# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_qso_bot', 'tg_qso_bot.bot', 'tg_qso_bot.models', 'tg_qso_bot.qso_sources']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'pyrogram>=0.17.1,<0.18.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['tg-qso-bot = tg_qso_bot.bot:main']}

setup_kwargs = {
    'name': 'tg-qso-bot',
    'version': '1.0.1',
    'description': 'Simple HAM helper bot written on Python',
    'long_description': '# tg-qso-bot\nSimple HAM helper bot written on Python.\n\n## Features\nBot may request QSO list from [Hamlog](https://hamlog.ru/) and print it to Telegram chat.\n\n## Installation\n```shell script\npython3 -m pip install tg-qso-bot\n```\n\n## Configuration\n1. Get `app_id` and `app_hash` from [Telegram Apps](https://my.telegram.org/apps).\nThe API key is personal and must be kept secret.\n2. Find telegram bot named `@botfarther`. Ask him existing bot token or create a new bot.\n3. Push `app_id`, `app_hash` and `bot_token` to file `config/settings.json`. You can\ncreate copy of this file for editing. It should be called `settings.local.json`.\n\n## Usage\n```shell script\npython3 -m tg_qso_bot.qso\n```\n',
    'author': 'exepirit',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exepirit/tg-qso-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
