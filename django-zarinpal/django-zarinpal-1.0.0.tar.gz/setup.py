# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_zarinpal', 'django_zarinpal.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-hashid-field>=3.1.1,<4.0.0', 'zeep>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'django-zarinpal',
    'version': '1.0.0',
    'description': 'integrate django payments with zarrinpal',
    'long_description': None,
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
