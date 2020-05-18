# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_onboarding',
 'netbox_onboarding.api',
 'netbox_onboarding.migrations',
 'netbox_onboarding.tests',
 'netbox_onboarding.utils']

package_data = \
{'': ['*'], 'netbox_onboarding': ['templates/netbox_onboarding/*']}

install_requires = \
['invoke>=1.4.1,<2.0.0', 'napalm>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'ntc-netbox-plugin-onboarding',
    'version': '0.9.1',
    'description': 'A plugin for NetBox to easily onboard new devices.',
    'long_description': '# NetBox Onboaring plugin\n\n<!-- Build status with linky to the builds for ease of access. -->\n[![Build Status](https://travis-ci.com/networktocode/ntc-netbox-plugin-onboarding.svg?token=29s5AiDXdkDPwzSmDpxg&branch=master)](https://travis-ci.com/networktocode/ntc-netbox-plugin-onboarding)\n\n<!-- TODO: https://github.com/networktocode/ntc-netbox-plugin-onboarding/issues/3\n\nImprove this readme with accurate descriptions of what this does, as well as\nappropriate links to rendered documentation and standard sections such as:\n\n## Installation\n\n## Usage\n\n## Contributing\n\n-->\n\n\n```\ninvoke --list\nAvailable tasks:\n\n  build            Build all docker images.\n  cli              Launch a bash shell inside the running NetBox container.\n  create-user      Create a new user in django (default: admin), will prompt for password\n  debug            Start NetBox and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  makemigrations   Run Make Migration in Django\n  nbshell          Launch a nbshell session.\n  start            Start NetBox and its dependencies in detached mode.\n  stop             Stop NetBox and its dependencies.\n```\n',
    'author': 'Info',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/networktocode/ntc-netbox-plugin-onboarding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
