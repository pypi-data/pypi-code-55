# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radcam']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.5.1,<8.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pillow>=7.1.2,<8.0.0',
 'plotly>=4.7.1,<5.0.0',
 'torch>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'radcam',
    'version': '1.0.0',
    'description': 'simple image perturber for CNN visualization',
    'long_description': None,
    'author': 'pdoyle5000',
    'author_email': 'pdoyle5000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
