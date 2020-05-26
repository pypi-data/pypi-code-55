# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['arcane-firebase==0.1.2',
 'firebase-admin>=4.1.0,<5.0.0',
 'google-cloud-pubsub>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'arcane-pubsub',
    'version': '0.2.1',
    'description': 'Overide pubsub client',
    'long_description': '# Arcane PubSub\n\nThis package is base on [google-cloud-pubsub](https://pypi.org/project/google-cloud-pubsub/).\n\n## Get Started\n\n```sh\npip install arcane-pubsub\n```\n\n## Example Usage\n\n```python\nfrom arcane import pubsub\n\n# Import your configs\nfrom configure import Config\n\nclient = pubsub.Client(Config.KEY)\n\nclient.push_to_topic(\'project\', \'topic\', {"parameter": "value"})\n```\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
