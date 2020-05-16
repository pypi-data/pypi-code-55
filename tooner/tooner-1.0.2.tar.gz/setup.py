# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tooner']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tooner',
    'version': '1.0.2',
    'description': 'An easier way to manage and launch sessions for Toontown Rewritten.',
    'long_description': 'An easier way to manage and launch sessions for multiple toons for [Toontown Rewritten](https://toontownrewritten.com).\n\n# What does it do?\n\nCurrently, it allows you to communicate with Toontown Rewritten\'s login API in order to log in and start a session with very few lines of code.\n\n```\nlauncher = multitooner.ToontownLauncher(directory="TTREngine.exe")\nlauncher.play(username="username", password="password")\n```\n\nIf you\'re crazy, you can even combine these lines into one!\n\nThe best part is that you can do this to **play multiple toons at once**.\n\n# Why does this exist?\n\nSince I normally play on MacOS, there is no way for me to open multiple sessions of the Toontown Rewritten launcher without doing it from the terminal; this was really annoying to do every time I wanted to multitoon (which is a lot), so I set out to make this easier.\n\nUltimately, I was successful in making this functionality work the three major operating systems: Windows, MacOS, and, I assume, on Linux (I haven\'t been able to test this).\n\n# Taking it further\n\nI have a few project ideas that could use this functionality:\n- Make a menu bar app for MacOS\n- Make a GUI to allow the user to store login information and start sessions for multiple toons\n- Refactor the launcher module to allow for better communication with the GUI\n- Send toast notifications for invasions\n- If multitooning, tile windows automatically\nHowever, they would be separate projects.\n\n# Authors\n- **Jake Brehm** - *Initial Work* - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)',
    'author': 'Jake Brehm',
    'author_email': 'mail@jakebrehm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
