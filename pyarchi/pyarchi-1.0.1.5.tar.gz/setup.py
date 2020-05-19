# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyarchi',
 'pyarchi.data_objects',
 'pyarchi.initial_detection',
 'pyarchi.masks_creation',
 'pyarchi.output_creation',
 'pyarchi.proof_concept',
 'pyarchi.routines',
 'pyarchi.star_track',
 'pyarchi.utils',
 'pyarchi.utils.data_export',
 'pyarchi.utils.factors_handler',
 'pyarchi.utils.image_processing',
 'pyarchi.utils.misc',
 'pyarchi.utils.noise_metrics',
 'pyarchi.utils.optimization']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0,<5.0',
 'matplotlib>=3.1.2,<4.0.0',
 'opencv-python>=4.1.2,<5.0.0',
 'pyyaml>=5.3,<6.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pyarchi',
    'version': '1.0.1.5',
    'description': "Photometry for CHEOPS's background stars",
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/archi/badge/?version=latest)](https://archi.readthedocs.io/en/latest/?badge=latest)\n# ARCHI - An expansion to the CHEOPS mission official pipeline\n\nCHEOPS mission, one of ESA\'s mission has been launched in December 2019. \n\nThe official pipeline released for this mission only works for the\ntarget star, thus leaving a lot of information  left to explore. Furthermore, the presence of background stars in our images\ncan mimic astrophysical signals in the target star. \n\n\nWe felt that there was a need for a pipeline capable of analysing those stars and thus, built archi, a pipeline\nbuilt on top of the DRP, to analyse those stars. Archi has been tested with simulated data, showing proper behaviour.\nON the target star we found photometric precisions either equal or slightly better than the DRP. For the background stars we found photometric preicision 2 to 3 times higher than the target star.\n\n# How to install archi \n\nThe pipeline is written in Python3, and most features should work on all versions. However, so far, it was only tested on python 3.6, 3.7 and 3.8\n\nTo install, simply do :\n\n    pip install pyarchi\n\n# How to use the library \n\nA proper introduction to the library, alongside documentation of the multiple functions and interfaces can be found [here](https://archi.readthedocs.io/en/latest/)\n\n\n# Known Problems\n\n\n [1] There is no correction for cross-contamination between stars\n [2] If we have data in the entire 200*200 region (not expected to happen) and using the "dynam" mask for the background stars it might "hit" one of the edges of the image. In such case, larger masks will not increase in the direction in which the edge is reached. However, the mask can still grow towards the other directions, leading to masks significantly larger than the original star. In such cases, we recommend to manually change the mask size on the "optimized factors" file.\n',
    'author': 'Kamuish',
    'author_email': 'amiguel@astro.up.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kamuish/archi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
