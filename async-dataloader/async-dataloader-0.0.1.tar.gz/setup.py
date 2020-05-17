# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataloader']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'async-dataloader',
    'version': '0.0.1',
    'description': 'Asyncio Dataloader for GraphQL.',
    'long_description': "# Async DataLoader\n\nAsync DataLoader is a python port of [DataLoader](https://github.com/graphql/dataloader).\n\nDataLoader is a generic utility to be used as part of your application's data fetching layer to provide a simplified and consistent API over various remote data sources such as databases or web services via batching and caching.\n\n## Requirement\n\nPython 3.7+\n\n## Installation\n\n`pip install async-dataloader`\n\n## Example\n\nPlease see this graphql [example](https://github.com/syfun/async-dataloader/tree/master/examples/post_tags.py).\n\n",
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/async-dataloader',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
