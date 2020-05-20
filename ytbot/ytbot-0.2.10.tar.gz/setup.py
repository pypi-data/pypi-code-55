# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytbot']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pyppeteer_stealth>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['ytbot = ytbot:main']}

setup_kwargs = {
    'name': 'ytbot',
    'version': '0.2.10',
    'description': 'A simple yet amazing bot for increasing youtube views and it works!!',
    'long_description': 'YTBOT\n\n## THIS BOT GENERATES GENUINE YOUTUBE VIEWS ##\n\n\n\n\nHow to install?\n\npip install ytbot\n\n\n\n\nwhat are the requirements?\n\n*python3.6 or above* \n*chromium-browser(developer version)*\n*A few google accounts(this is important)\n*a little bit of patience*\n\n\nI tried my best to make it as user friendly as possible. But you should find bugs here and there. I\'m still testing the capabilities of this bot. So, I don\'t know for sure if it would work for everyone. But it won\'t be a garbage I assure you.\n\n\nHow to use it?\n\nOnce installed ytbot, go to the terminal and write "ytbot configure" then follow the instructions there.\nYou will need to provide the path to a chromium-browser that you installed(developer version of course)\nafter that, add a few google accounts(remember to give right infos) it\'s necessary because of the way this bot works. The mechanics is like that you get 1 view per account every 10 minutes. So, 10 account means 10 views per 10 minutes. 20 account means 20 views per 10 minutes! and so on. Cool right?\nBut beware! It will eat alot of ram.\nthen it will ask for youtube video url. provide as many as you want.But keep the number less than 10 for better performance. \n\nWhen the configuration is complete, run the bot symply by "ytbot run" or "ytbot run -h" for headless.\n\n\n',
    'author': 'Muhammad Fahim',
    'author_email': 'muhammadfahim010@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adnangif/ytbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
