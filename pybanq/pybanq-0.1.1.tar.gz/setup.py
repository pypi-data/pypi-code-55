# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybanq',
 'pybanq.asi',
 'pybanq.asi.deepRL',
 'pybanq.asi.deepRL.games',
 'pybanq.asi.deepRL.games.connect4',
 'pybanq.asi.deepRL.games.metasquares',
 'pybanq.asi.deepRL.run',
 'pybanq.asi.deepRL.run.logs',
 'pybanq.asi.deepRL.run.memory',
 'pybanq.asi.deepRL.run.models',
 'pybanq.block',
 'pybanq.nano',
 'pybanq.quantum']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.3.1,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'nltk>=3.5,<4.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'pybanq',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jachiike Madubuko',
    'author_email': 'jachiike.madubuko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
