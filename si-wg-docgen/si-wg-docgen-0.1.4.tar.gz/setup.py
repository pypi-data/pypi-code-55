# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['si_wg_docgen', 'si_wg_docgen.bin']

package_data = \
{'': ['*'], 'si_wg_docgen': ['data/*']}

install_requires = \
['mistletoe>=0.7.2,<0.8.0', 'owlrl>=5.2.1,<6.0.0', 'rdflib>=5.0,<6.0']

entry_points = \
{'console_scripts': ['make_docx = si_wg_docgen.bin.make_docx:generate']}

setup_kwargs = {
    'name': 'si-wg-docgen',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
