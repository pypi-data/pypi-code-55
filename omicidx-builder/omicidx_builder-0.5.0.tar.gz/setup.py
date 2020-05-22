# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicidx_builder',
 'omicidx_builder.data',
 'omicidx_builder.data.bigquery_schemas']

package_data = \
{'': ['*']}

install_requires = \
['Click',
 'asyncpg>=0.20.0,<0.21.0',
 'databases>=0.2.6,<0.3.0',
 'elasticsearch>=7,<8',
 'elasticsearch_dsl>=7,<8',
 'google-cloud-bigquery',
 'google-cloud-pubsub',
 'google-cloud-storage',
 'kubernetes>=10.0.1,<11.0.0',
 'omicidx==0.3.10',
 'psycopg2>=2.8,<3.0',
 'pydantic>=1.1,<2.0',
 'sqlalchemy>=1.3,<2.0',
 'toml>=0.10,<0.11',
 'ujson>=1.35,<2.0']

entry_points = \
{'console_scripts': ['omicidx_builder = omicidx_builder.cli:cli']}

setup_kwargs = {
    'name': 'omicidx-builder',
    'version': '0.5.0',
    'description': 'Tooling to build and deploy omicidx data and resources',
    'long_description': None,
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seandavi/omicidx-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
