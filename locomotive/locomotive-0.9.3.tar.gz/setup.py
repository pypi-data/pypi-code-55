# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locomotive',
 'locomotive.api',
 'locomotive.cli',
 'locomotive.cli.commands',
 'locomotive.cli.templates',
 'locomotive.data',
 'locomotive.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0',
 'click>=7.0,<8.0',
 'colored>=1.4.2,<2.0.0',
 'dateparser>=0.7,<0.8',
 'faker>=3.0.0,<4.0.0',
 'geopy>=1.20,<2.0',
 'jinja2>=2.11.1,<3.0.0',
 'pendulum>=2.0.5,<3.0.0',
 'py-money>=0.4.0,<0.5.0',
 'requests>=2.20,<3.0',
 'tableformatter>=0.1.4,<0.2.0',
 'text-unidecode>=1.3,<2.0',
 'tqdm>=4.42.1,<5.0.0']

entry_points = \
{'console_scripts': ['locomotive = locomotive.cli:cli']}

setup_kwargs = {
    'name': 'locomotive',
    'version': '0.9.3',
    'description': "Python API clients and a CLI for France's railways.",
    'long_description': '<p align="center">\n  <img src="/docs/_assets/logo.png" height="150"><br/>\n  <i>Python API clients and a CLI for France\'s railways :sparkles:</i><br/><br/>\n  <a href="https://maxmouchet.github.io/locomotive">\n    <img src="https://img.shields.io/badge/docs-master-blue.svg?style=flat">\n  </a>\n  <a href="https://github.com/maxmouchet/locomotive/actions">\n    <img src="https://github.com/maxmouchet/locomotive/workflows/CI/badge.svg">\n  </a>\n  <a href="https://coveralls.io/github/maxmouchet/locomotive?branch=master">\n    <img src="https://coveralls.io/repos/github/maxmouchet/locomotive/badge.svg?branch=master&service=github">\n  </a>\n</p>\n\n<p align="center">\n  <img src="/docs/_assets/screen_search.png" width="800px">\n  <img src="/docs/_assets/screen_live.png" width="800px">\n</p>\n\n## Installation\n\n`locomotive` requires Python 3.6+ and can be installed using [pip](https://pip.pypa.io/en/stable/):\n\n```bash\npip install locomotive\n```\n\n## API Clients\n\nModule | Features | Status\n-------|----------|-------\n[oui_v3](/locomotive/api/oui_v3.py) | Travel Request | ![oui_v3](https://github.com/maxmouchet/locomotive/workflows/oui_v3/badge.svg)\n[gc](/locomotive/api/gc.py) | Board Request | ![oui_v3](https://github.com/maxmouchet/locomotive/workflows/gc/badge.svg)\n\n## CLI\n\nlocomotive is easy to use. Find below simple examples:\n\n```bash\nlocomotive search --help\n# Search by city name\nlocomotive search Amsterdam Paris\n# Search by train station code (Amsterdam to Paris here)\nlocomotive search NLAMA FRPAR\n# Specify the date and the travel class\nlocomotive search Brest Paris --date 2019/07/14 --class first\n```\n\n## Development\n\n```bash\npoetry install\npoetry run locomotive\n\n# pre-commit\npoetry run pre-commit install\npoetry run pre-commit run --all-files\n```\n\n### Releases\n\n```bash\npoetry version X.Y.Z # e.g. v0.4.0\ngit tag vX.Y.Z\ngit push --tags\n```\n\n## Licenses\n\nlocomotive is released under the [MIT license](https://github.com/maxmouchet/locomotive/blob/master/LICENSE).\nThe train stations database (`stations-lite.csv`) is derived from `stations.csv` ([trainline-eu/stations](https://github.com/trainline-eu/stations)) released under the Open Database License (ODbL) license.\n\n*Logo: Train Tickets by b farias from the Noun Project.*\n',
    'author': 'Yann Feunteun, Maxime Mouchet',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmouchet/locomotive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
