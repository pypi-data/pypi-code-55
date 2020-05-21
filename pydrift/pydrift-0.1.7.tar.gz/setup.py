# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydrift', 'pydrift.test']

package_data = \
{'': ['*'], 'pydrift': ['core/*']}

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
    'version': '0.1.7',
    'description': 'How do we measure the degradation of a machine learning process? Why does the performance of our predictive models decrease? Maybe it is that a data source has changed (one or more variables) or maybe what changes is the relationship of these variables with the target we want to predict. `pydrift` tries to facilitate this task to the data scientist, performing this kind of checks and somehow measuring that degradation.',
    'long_description': '# Welcome to `pydrift` 0.1.7\n\nHow do we measure the degradation of a machine learning process? Why does the performance of our predictive models decrease? Maybe it is that a data source has changed (one or more variables) or maybe what changes is the relationship of these variables with the target we want to predict. `pydrift` tries to facilitate this task to the data scientist, performing this kind of checks and somehow measuring that degradation.\n\n# Install `pydrift` :v:\n\n`pip install pydrift`\n\n# Structure :triangular_ruler:\n\nThis is intended to be user-friendly. pydrift is divided into **DataDriftChecker** and **ModelDriftChecker**:\n\n- **DataDriftChecker**: search for drift in the variables, check if their distributions have changed\n- **ModelDriftChecker**: search for drift in the relationship of the variables with the target, checks that the model behaves the same way for both data sets\n\nBoth can use a discriminative model (defined by parent class **DriftChecker**), where the target would be binary in belonging to one of the two sets, 1 if it is the left one and 0 on the contrary. If the model is not able to differentiate given the two sets, there is no difference!\n\n![Class inheritance](https://raw.githubusercontent.com/sergiocalde94/Data-And-Model-Drift-Checker/master/images/class_inheritance.png)\n\nIt also exists `InterpretableDrift` that manages all of the stuff related to interpretability of drifting. It can show us the features distribution or the most important features when we are training a discriminative model or our predictive one.\n\n# Usage :book:\n\nYou can take a look to the `notebooks` folder where you can find one example for generic `DriftChecker`, one for DataDriftChecker` and other one for `ModelDriftChecker`. \n\n# Correct Notebooks Render :bulb:\n\nBecause `pydrift` uses plotly and GitHub performs a static render of the notebooks figures do not show correctly. For a rich view of the notebook, you can visit  [nbviewer](http://nbviewer.jupyter.org/) and paste the link to the notebook you want to show, for example if you want to render **1-Titanic-Drift-Demo.ipynb** you have to paste https://github.com/sergiocalde94/Data-And-Model-Drift-Checker/blob/master/notebooks/1-Titanic-Drift-Demo.ipynb into nbviewer.  \n\n# More Info :information_source:\n\nFor more info check the docs available [here](https://sergiocalde94.github.io/Data-And-Model-Drift-Checker/)\n\nMore demos and code improvements will coming, if you want to contribute you can contact me (sergiocalde94@gmail.com), in the future I will upload a file to explain how this would work.\n',
    'author': 'sergiocalde94',
    'author_email': 'sergiocalde94@gmail.com',
    'url': 'https://github.com/sergiocalde94/Data-And-Model-Drift-Checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
