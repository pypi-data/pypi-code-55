# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rchat']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'confight>=1.3.1,<2.0.0',
 'rocketchat-API>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['rchat = rchat.cli:cli']}

setup_kwargs = {
    'name': 'rchat',
    'version': '0.0.2',
    'description': 'A simple RocketChat command line client',
    'long_description': '# rchat\n![build](https://github.com/jvrsantacruz/rchat/workflows/build/badge.svg)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\nA simple RocketChat command line client\n\n    rchat --to #team "Hello World!"\n\n## Usage\n\n_rchat_ comes with a command line interface that allows you to send messages\neither to groups or direct people:\n\n    rchat --to @rita.cantaora "Hi Rita!"\n\nThe message can also be piped into the program via stdin:\n\n    echo "Hi!" | rchat --to #team\n\nSee help for more information:\n\nSee `rchat --help`.\n\n## Configuration\n\n_rchat_ needs to know at least the server url and user credentials to use the\nAPI. Those parameters can be given via _command line option_, set using an\n_envvar_ or by setting them in a _config file_.\n\nBase configuration options can be taken from the command line.\nArguments given in the command line will override any other configuration.\n\n    --user TEXT      Username in RocketChat\n    --user-id TEXT   User id associated to a Token\n    --token TEXT     Personal Acces Token Name\n    --password TEXT  Password for user in RocketChat\n    --url TEXT       Url to the RocketChat server\n\nThey can also be set as a environment variable by prefixing them such as\n`RCHAT_URL`. Arguments set this way will take precedence over the ones in the\nconfig file.\n\nTo configure via file, place your parameters in [toml][] format at\n`~/.config/rchat/config.toml`:\n\n```toml\n[rchat]\nuser_id = \'a1d3f4dd..\'\ntoken = \'fjXkkf..\'\nurl = \'https://rocketchat.myserver.net\'\n```\n\nA specific config file can be given by passing the `--config` option or setting\nthe `RCHAT_CONFIG` envvar.\n\nExtra config files can be placed in the `conf.d` directory and all of them will\nbe merged together using [confight](https://github.com/avature/confight). Last\nvalues found in these files will override the previous ones, so the complete\nlist of places to be searched, in the order that will be read are:\n\n- `/etc/rchat/config.toml`\n- `/etc/rchat/conf.d/*`\n- `~/.config/rchat/config.toml`\n- `~/.config/rchat/conf.d`\n\nMeaning that the keys in files placed at `~/.config/rchat/conf.d` will override\nthe rest.\n\n[toml]: https://github.com/toml-lang/toml\n\n## Development\n\nFrom the root of the application directory, create a python environment,\ninstall the application in development mode along with its dependencies and\nrun it locally:\n\n    virtualenv env\n    . env/bin/activate\n    pip install --upgrade pip\n    pip install -e . -r requirements.txt -r dev-requirements.txt\n\nTests can be run using *tox* (recommended):\n\n    pip install tox\n    tox\n\nOr directly by calling *py.test*:\n\n    python -m pytest\n\n## TODO\n\n- [X] Send private messages\n- [X] Send message from stdin\n- [X] Send message from files\n- [ ] Upload files\n- [ ] Upload images\n- [ ] Read messages\n- [ ] Listen to new messages\n- [ ] Autocomplete emojis\n- [ ] Autocomplete users\n- [ ] Autocomplete channels\n- [ ] Config file\n- [ ] Logging and debug\n- [ ] Debian Packaging\n- [ ] Bundled Packaging\n- [ ] Pypi version\n- [ ] Versioning script\n- [ ] Improve startup time\n- [ ] Define groups of users\n- [ ] Allow to get reactions\n- [ ] Allow for threads\n- [ ] Implement (pre|post) message hooks\n- [ ] Implement (pre|post) reaction hooks\n- [ ] Autocomplete names\n- [ ] Autocomplete channels\n- [ ] Open editor to compose message\n- [ ] Preview message in markdown viewer\n- [ ] Autoformat input as verbatim\n',
    'author': 'Javier Santacruz',
    'author_email': 'javier.santacruz.lc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jvrsantacruz/rchat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
