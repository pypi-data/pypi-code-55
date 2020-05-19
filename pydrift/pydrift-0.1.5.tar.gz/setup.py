# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydrift', 'pydrift.test']

package_data = \
{'': ['*'], 'pydrift': ['catboost_info/*', 'catboost_info/learn/*', 'core/*']}

install_requires = \
['catboost>=0.23,<0.24',
 'coveralls>=2.0.0,<3.0.0',
 'flake8>=3.8.1,<4.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'missingno>=0.4.2,<0.5.0',
 'pandas>=1.0.3,<2.0.0',
 'plotly_express>=0.4.1,<0.5.0',
 'pre-commit>=2.4.0,<3.0.0',
 'pytest>=5.4.2,<6.0.0',
 'shap>=0.35.0,<0.36.0',
 'sklearn>=0.0,<0.1',
 'sphinx>=3.0.3,<4.0.0',
 'sphinx_press_theme>=0.5.1,<0.6.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pydrift',
    'version': '0.1.5',
    'description': 'How do we measure the degradation of a machine learning process? Why does the performance of our predictive models decrease? Maybe it is that a data source has changed (one or more variables) or maybe what changes is the relationship of these variables with the target we want to predict. `pydrift` tries to facilitate this task to the data scientist, performing this kind of checks and somehow measuring that degradation.',
    'long_description': None,
    'author': 'sergiocalde94',
    'author_email': 'sergiocalde94@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
