# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['braincube_token_getter']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0', 'pyopenssl>=19.1.0,<20.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['braincube-token-getter = braincube_token_getter:run']}

setup_kwargs = {
    'name': 'braincube-token-getter',
    'version': '0.0.1',
    'description': 'A utility to get a braincube token',
    'long_description': '# Braincube Token Getter\n\nBraincube Token Getter is small program that uses the braincube sso in order to obtain a temporary token.\n\nThe program uses the flask python framework.\n\n## Installation\n\n```bash\npip install braincube-token-getter\n```\n\n## Usage\n\n### Create a new configuration\n\nBy default the new configuration is stored in `~/.braincube/`  but the option `-d` can be used to specify a specific configuration directory.\n\n```bash\nbraincube-token-getter -c -d my_directory\n```\n\nThe program will ask for a Baincube application *Client ID*  and *Client Secret*. If you do not know how to find these informations or how to create a Braincube application, see the section *Create a Braincube application*.\n\n### Request a token\n\n```bash\nbraincube-token-getter -t\n```\n\nThe token is added to the `my_directory/config.json` file.\n\nNote: your browser may warn you with a Security risk because your ssl certificate is not known by firefox or chrome. In this case click on `Advanced...` and `Accept the Risk an Continue`.\n\n## Create a Braincube application\n\n1. Connect to [mybraincube.com/](https://mybraincube.com/)\n\n2. Go to `Configure` by clicking on you *username* on the top left corner.\n3. Go to application on the thin horizontal menu bar just below the black header.\n4. Either select an existing application you want to use or create a new one with the +/- icon.\n5. Note that the url of your application should be `https://localhost:5000/token` so that the program gets the right url when it logs in.\n',
    'author': 'Braincube',
    'author_email': 'io@braincube.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
