# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbbmon']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['bbbmon = bbbmon.bbbmon:main']}

setup_kwargs = {
    'name': 'bbbmon',
    'version': '0.1.25',
    'description': 'A small CLI utility to monitor bbb usage',
    'long_description': "# bbbmon\n\nA small python based CLI utility to monitor BigBlueButton-Usage. \n\n## Installation\n\nThe easiest way to install bbbmon is to install it from the Python Package Index (PyPi). This project uses [python poetry](https://python-poetry.org/) for dependency management, so you could also run it without installing the package system wide, see instructions below.\n\n## Install with pip3\n\n```bash\nsudo pip3 install bbbmon --upgrade\n```\n\nThen run with:\n\n```bash\nbbbmon\n```\n\n## Run with poetry (without pip)\n\nClone the repo:\n\n```bash\ngit clone https://code.hfbk.net/bbb/bbbmon.git\n```\n\nMake sure you have poetry installed. Install instruction for poetry can be [found here](https://python-poetry.org/docs/#installation).\nFrom inside the project directory run:\n\n```bash\npoetry install\n```\n\nRun bbbmon with:\n\n```bash\npoetry run bbbmon\n```\n\n\n\n# Configuration\n\nRun `bbbmon config --new` to create a new default configuration file. bbbmon will always ask you before it creates or overwrites anything.\n\nWithin the config you can define one or more endpoints with running bbb instances – each with it's secret and bigbluebutton-URL. You can find the secret on your server in it's config-file via \n\n```bash\ncat /usr/share/bbb-web/WEB-INF/classes/bigbluebutton.properties | grep securitySalt=\n```\n\nA example configuration file could look like this:\n```toml\n[bbb.example.com]\nsecuritySalt=MY_SUPER_SECRET_SECRET\nbigbluebutton.web.serverURL=https://bbb.example.com/\n\n[Föö]\nsecuritySalt=MY_SUPER_SECRET_SECRET2\nbigbluebutton.web.serverURL=https://bbb.foo.com/\n```\nThe section names in the square brackets can be chosen arbitrarily (as long as they are unique) and will be used as display names (they support utf-8). It makes sense to keep them short as they can be  used for filtering and/or ordering:\n\n```bash\nbbbmon meetings -e Föö\n```\n\n\n\n# Usage\n\nFor help run:\n\n```bash\nbbbmon -h\n```\n\nbbbmon supports command abbreviations – these commands produce the same result:\n\n```bash\nbbbmon meetings\nbbbmon meeting\nbbbmon mee\nbbbmon m\n```\n\nThis works as long as there is no other command starting with the same letters.",
    'author': 'David Huss',
    'author_email': 'david.huss@hfbk-hamburg.de',
    'maintainer': 'David Huss',
    'maintainer_email': 'david.huss@hfbk-hamburg.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
