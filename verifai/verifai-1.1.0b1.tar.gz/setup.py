# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verifai',
 'verifai.features',
 'verifai.samplers',
 'verifai.simulators',
 'verifai.simulators.car_simulator',
 'verifai.simulators.car_simulator.examples',
 'verifai.simulators.car_simulator.examples.control_utils',
 'verifai.simulators.car_simulator.examples.lanekeeping_LQR',
 'verifai.simulators.carla',
 'verifai.simulators.carla.agents',
 'verifai.simulators.openai_gym',
 'verifai.simulators.webots',
 'verifai.simulators.xplane',
 'verifai.simulators.xplane.utils',
 'verifai.tests',
 'verifai.utils']

package_data = \
{'': ['*'], 'verifai.simulators.car_simulator': ['imgs/*']}

install_requires = \
['dill>=0.3.1,<0.4.0',
 'dotmap>=1.3.13,<2.0.0',
 'easydict>=1.9,<2.0',
 'future>=0.18.2,<0.19.0',
 'joblib>=0.14.1,<0.15.0',
 'matplotlib>=3.2.1,<4.0.0',
 'metric-temporal-logic>=0.1.5,<0.2.0',
 'numpy>=1.18.2,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pygame>=1.9.6,<2.0.0',
 'scenic>=1.1.0-beta.1,<2.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'scipy>=1.4.1,<2.0.0']

extras_require = \
{'bayesopt': ['GPy>=1.9.9,<2.0.0', 'GPyOpt>=1.2.6,<2.0.0'],
 'dev': ['pytest>=5.4.1,<6.0.0',
         'pytest-randomly>=3.2.1,<4.0.0',
         'tox>=3.14.0,<4.0.0',
         'sphinx>=2.4.4,<3.0.0',
         'sphinx-autodoc-typehints>=1.10.3,<2.0.0',
         'sphinx-rtd-theme>=0.4.3,<0.5.0',
         'recommonmark>=0.6.0,<0.7.0'],
 'examples': ['tensorflow>=1.8.0,<2.0.0',
              'gym>=0.17.1,<0.18.0',
              'baselines>=0.1.5,<0.2.0',
              'opencv-python>=4.2.0,<5.0.0',
              'Pillow>=7.0.0,<8.0.0']}

setup_kwargs = {
    'name': 'verifai',
    'version': '1.1.0b1',
    'description': 'A toolkit for the formal design and analysis of systems that include artificial intelligence (AI) and machine learning (ML) components.',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/verifai/badge/?version=latest)](https://verifai.readthedocs.io/en/latest/?badge=latest)\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\n\n# VerifAI\n\n**VerifAI** is a software toolkit for the formal design and analysis of \nsystems that include artificial intelligence (AI) and machine learning (ML)\ncomponents.\nVerifAI particularly seeks to address challenges with applying formal methods to perception and ML components, including those based on neural networks, and to model and analyze system behavior in the presence of environment uncertainty.\nVerifAI’s core paradigm, simulation guided by formal models and specifications, enables a variety of use cases including temporal-logic falsification, model-based systematic fuzz testing, parameter synthesis, counterexample analysis, and data set augmentation.\n\nPlease see the [documentation](https://verifai.readthedocs.io/) for installation instructions, tutorials, publications using VerifAI, and more.\n\nVerifAI was designed and implemented by Tommaso Dreossi, Daniel J. Fremont, Shromona Ghosh, Edward Kim, Hadi Ravanbakhsh, Marcell Vazquez-Chanlatte, and Sanjit A. Seshia.\n\nIf you have any problems using VerifAI, please submit an issue to the GitHub repository or contact Daniel Fremont at [dfremont@ucsc.edu](mailto:dfremont@ucsc.edu) or Edward Kim at [ek65@berkeley.edu](mailto:ek65@berkeley.edu).\n\n### Repository Structure\n\n* _docs_: sources for the [documentation](https://verifai.readthedocs.io/);\n\n* _examples_: examples and additional documentation for particular simulators, including CARLA, Webots, X-Plane, and OpenAI Gym;\n\n* _verifai_: the source for the `verifai` package proper.',
    'author': 'Tommaso Dreossi',
    'author_email': None,
    'maintainer': 'Daniel Fremont',
    'maintainer_email': 'dfremont@ucsc.edu',
    'url': 'https://github.com/BerkeleyLearnVerify/VerifAI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
