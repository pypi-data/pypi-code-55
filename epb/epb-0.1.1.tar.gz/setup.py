# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'epb',
    'version': '0.1.1',
    'description': 'Energy performance of buildings',
    'long_description': '# Energy performance of buildings\n\nThis library provides helpers for energy performance of buildings computation.\n\n## Installing\n\n### With PIP\n\n```sh\npip install epb\n```\n\n### With Poetry\n\n```sh\npoetry add epb\n```\n\n## Usage\n\n```py\nfrom epb.utils import Regulator, energy_class, total_consumption\n\n\neclass = energy_class(Regulator.BRUSSELS, 100)\n# eclass == "C+"\n\n\ntconsum = total_consumption(100, 250)\n# tconsum == 25_000\n```\n',
    'author': 'Arthur White',
    'author_email': 'arthur@white.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/immoveable/epb-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
