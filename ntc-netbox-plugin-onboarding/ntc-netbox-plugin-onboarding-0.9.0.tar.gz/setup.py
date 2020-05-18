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
    'version': '0.9.0',
    'description': 'A plugin for NetBox to easily onboard new devices.',
    'long_description': None,
    'author': 'Info',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
