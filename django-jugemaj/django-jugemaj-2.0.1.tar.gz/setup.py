# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jugemaj', 'jugemaj.migrations', 'jugemaj.templatetags']

package_data = \
{'': ['*'], 'jugemaj': ['templates/*', 'templates/jugemaj/*']}

install_requires = \
['ndh>=3.10.4,<4.0.0']

setup_kwargs = {
    'name': 'django-jugemaj',
    'version': '2.0.1',
    'description': 'A Django app for the Majority Judgment voting system',
    'long_description': '# Jugement Majoritaire\n[![Build Status](https://travis-ci.org/nim65s/django-jugemaj.svg?branch=master)](https://travis-ci.org/nim65s/django-jugemaj)\n[![Coverage Status](https://coveralls.io/repos/github/nim65s/django-jugemaj/badge.svg?branch=master)](https://coveralls.io/github/nim65s/django-jugemaj?branch=master)\n\n\nApplication de vote par [Jugement Majoritaire](https://fr.wikipedia.org/wiki/Jugement_majoritaire).\n\n\n## Requirements\n\n- [ndh](https://pypi.python.org/pypi/ndh) (which requires [django](https://www.djangoproject.com/),\n  [django-autoslug](https://github.com/justinmayer/django-autoslug/),\n  [django-bootstrap4](https://github.com/zostera/django-bootstrap4) (can be made optional on request))\n\nTested with:\n- Python 3.6, 3.7, 3.8\n- [Django](https://www.djangoproject.com/) 2.0, 2.1, 2.2, 3.0\n\n## Theory\n\n- [A theory of measuring, electing, and ranking. *Michel Balinski and Rida Laraki*. In PNAS 2007](https://doi.org/10.1073/pnas.0702634104)\n- [Majority Judgment vs Majority Rule, *Michel Balinski and Rida Laraki*](http://www.lamsade.dauphine.fr/sites/default/IMG/pdf/cahier_377.pdf)\n',
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nim65s/django-jugemaj',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
