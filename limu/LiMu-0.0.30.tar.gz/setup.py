# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['limu']
install_requires = \
['hdbscan>=0.8,<0.9',
 'numpy>=1.18,<2.0',
 'pandas>=1.0,<2.0',
 'rawkit>=0.6,<0.7',
 'scikit-image>=0.16,<0.17',
 'scikit-learn>=0.22,<0.23',
 'scipy>=1.4,<2.0']

entry_points = \
{'console_scripts': ['limu = limu:cli']}

setup_kwargs = {
    'name': 'limu',
    'version': '0.0.30',
    'description': 'Tool to analyse images of cleared and trypan blue stained leaves to assess leaf damage.',
    'long_description': '\nTool to analyse images of cleared and trypan blue stained leaves to assess leaf damage.\n\ncurrently the program is under redevelopment and should be considered experimental alpha software. We are currently reimplementing most parts of code, use limu_original.py for now. Original code is however made for our specific data and needs changes to work for your data. \n\nlimu_original.py is the program used for the original publication\n\nMulaosmanovic, E., Lindblom, T.U.T., Bengtsson, M., Windstam, S.T., Mogren, L., Marttila, S., Stützel, H., Alsanius, B.W., 2020. High-throughput method for detection and quantification of lesions on leaf scale based on trypan blue staining and digital image analysis. Plant Methods 16, 62. https://doi.org/10.1186/s13007-020-00605-5\n\n\n\n\n',
    'author': 'Tobias U. T. Lindblom',
    'author_email': None,
    'maintainer': 'Tobias U. T. Lindblom',
    'maintainer_email': 'tobias.lindblom@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
