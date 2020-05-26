# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lipo']

package_data = \
{'': ['*']}

install_requires = \
['dlib>=19.19.0,<20.0.0', 'scikit-learn>=0.22.1', 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'lipo',
    'version': '1.2.1',
    'description': 'Global, derivative-free optimization',
    'long_description': 'LIPO is a package for derivative-free, global optimization. Is based on\nthe `dlib` package and provides wrappers around its optimization routine.\n\nThe algorithm outperforms random search - sometimes by margins as large as 10000x. It is often preferable to \nBayesian optimization which requires "tuning of the tuner". Performance is on par with moderately to well tuned Bayesian \noptimization.\n\nThe provided implementation has the option to automatically enlarge the search space if bounds are found to be \ntoo restrictive (i.e. the optimum being to close to one of them).\n\nSee the [LIPO algorithm implementation](http://dlib.net/python/index.html#dlib.find_max_global) for details.\n\nA [great blog post](http://blog.dlib.net/2017/12/a-global-optimization-algorithm-worth.html) by the author of \n`dlib` exists, describing how it works.\n\n# Installation\n\nExecute\n\n`pip install lipo`\n\n# Usage\n\n```python\nfrom lipo import GlobalOptimizer\n\ndef function(x, y, z):\n    zdict = {"a": 1, "b": 2}\n    return -((x - 1.23) ** 6) + -((y - 0.3) ** 4) * zdict[z]\n\npre_eval_x = dict(x=2.3, y=13, z="b")\nevaluations = [(pre_eval_x, function(**pre_eval_x))]\n\nsearch = GlobalOptimizer(\n    function,\n    lower_bounds={"x": -10.0, "y": -10},\n    upper_bounds={"x": 10.0, "y": -3},\n    categories={"z": ["a", "b"]},\n    evaluations=evaluations,\n    maximize=True,\n)\n\nnum_function_calls = 1000\nsearch.run(num_function_calls)\n```\n\nThe optimizer will automatically extend the search bounds if necessary.\n\nFurther, the package provides an implementation of the scikit-learn interface for \nhyperparamter search.\n\n```python\nfrom lipo import LIPOSearchCV\n\nsearch = LIPOSearchCV(\n    estimator,\n    param_space={"param_1": [0.1, 100], "param_2": ["category_1", "category_2"]},\n    n_iter=100\n)\nsearch.fit(X, y)\nprint(search.best_params_)\n```',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdb78/lipo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
