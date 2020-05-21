# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sklearn_nature_inspired_algorithms',
 'sklearn_nature_inspired_algorithms.helpers',
 'sklearn_nature_inspired_algorithms.model_selection']

package_data = \
{'': ['*']}

install_requires = \
['NiaPy==2.0.0rc10',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'seaborn>=0.10.1,<0.11.0',
 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'sklearn-nature-inspired-algorithms',
    'version': '0.4.1',
    'description': 'Search using nature inspired algorithms over specified parameter values for an sklearn estimator.',
    'long_description': '# Nature Inspired Algorithms for scikit-learn\n\n[![CI](https://github.com/timzatko/Sklearn-Nature-Inspired-Algorithms/workflows/CI/badge.svg?branch=master)](https://github.com/timzatko/Sklearn-Nature-Inspired-Algorithms/actions?query=workflow:CI+branch:master)\n[![Maintainability](https://api.codeclimate.com/v1/badges/ed99e5c765bf5c95d716/maintainability)](https://codeclimate.com/github/timzatko/Sklearn-Nature-Inspired-Algorithms/maintainability)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sklearn-nature-inspired-algorithms)\n[![PyPI version](https://badge.fury.io/py/sklearn-nature-inspired-algorithms.svg)](https://pypi.org/project/sklearn-nature-inspired-algorithms/)\n[![PyPI downloads](https://img.shields.io/pypi/dm/sklearn-nature-inspired-algorithms)](https://pypi.org/project/sklearn-nature-inspired-algorithms/)\n \nNature inspired algorithms for hyper-parameter tuning of [scikit-learn](https://github.com/scikit-learn/scikit-learn) models. This package uses algorithms implementation from [NiaPy](https://github.com/NiaOrg/NiaPy). \n\n## Installation\n\n```shell script\npip install sklearn-nature-inspired-algorithms\n```\n\n## Usage\n\nThe usage is similar to using sklearn\'s `GridSearchCV`.\n\n```python\nfrom sklearn_nature_inspired_algorithms.model_selection import NatureInspiredSearchCV\nfrom sklearn.ensemble import RandomForestClassifier\n\nparam_grid = { \n    \'n_estimators\': range(20, 100, 20), \n    \'max_depth\': range(2, 40, 2),\n    \'min_samples_split\': range(2, 20, 2), \n    \'max_features\': ["auto", "sqrt", "log2"],\n}\n\nclf = RandomForestClassifier(random_state=42)\n\nnia_search = NatureInspiredSearchCV(\n    clf,\n    param_grid,\n    algorithm=\'hba\', # hybrid bat algorithm\n    population_size=50,\n    max_n_gen=100,\n    max_stagnating_gen=10,\n    runs=3,\n    random_state=None, # or any number if you want same results on each run\n)\n\nnia_search.fit(X_train, y_train)\n```\n\nJupyter notebooks with full examples are available in [here](examples/notebooks).\n\n### Using custom nature inspired algorithm\n\nIf you do not want to use ony of the pre-defined algorithm configurations, you can use any algorithm from the  [NiaPy](https://github.com/NiaOrg/NiaPy) collection.\nThis will allow you to have more control of the algorithm behaviour. \nRefer to their [documentation](https://niapy.readthedocs.io/en/latest/) and [examples](https://github.com/NiaOrg/NiaPy/tree/master/examples) for the usage. \n\n```python\nfrom NiaPy.algorithms.basic import GeneticAlgorithm\n\nalgorithm = GeneticAlgorithm() # when custom algorithm is provided random_state is ignored\nalgorithm.setParameters(NP=50, Ts=5, Mr=0.25)\n\nnia_search = NatureInspiredSearchCV(\n    clf,\n    param_grid,\n    algorithm=algorithm,\n    population_size=50,\n    max_n_gen=100,\n    max_stagnating_gen=20,\n    runs=3,\n)\n\nnia_search.fit(X_train, y_train)\n```\n\n## Contributing \n\nDetailed information on the contribution guidelines are in the [CONTRIBUTING.md](./CONTRIBUTING.md).',
    'author': 'Timotej Zatko',
    'author_email': 'timi.zatko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timzatko/Sklearn-Nature-Inspired-Algorithms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
