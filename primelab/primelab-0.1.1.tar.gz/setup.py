# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['primelab']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.3,<2.0.0', 'scipy>=1.4.1,<2.0.0', 'sklearn>=0.0,<0.1']

extras_require = \
{'docs': ['sphinx>=3.0.2,<4.0.0',
          'nbsphinx>=0.6.1,<0.7.0',
          'ipykernel>=5.2.1,<6.0.0',
          'jupyter_client>=6.1.3,<7.0.0']}

setup_kwargs = {
    'name': 'primelab',
    'version': '0.1.1',
    'description': 'Numerical differentiation in python.',
    'long_description': '.. image:: https://readthedocs.org/projects/prime/badge/?version=latest\n   :target: https://prime.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n  \n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n   :target: https://lbesson.mit-license.org/\n   :alt: MIT License\n \nNumerical differentiation methods for python, including:\n\n1. Symmetric finite difference schemes using arbitrary window size. \n\n2. Savitzky-Galoy derivatives of any polynomial order with independent left and right window parameters.\n\n3. Spectral derivatives with optional filter.\n\n4. Spline derivatives of any order.\n\n5. Polynomial-trend-filtered derivatives generalizing methods like total variational derivatives. \n\nThese examples are intended to survey some common differentiation methods. The goal of this package is to bind these common differentiation methods to an easily implemented differentiation interface to encourage user adaptation.\n\nUsage:\n\n.. code-block:: python\n\n    from primelab import dxdt\n    import numpy as np\n\n    t = np.linspace(0,2*np.pi,50)\n    x = np.sin(x)\n\n    # Finite differences with central differencing using 3 points.\n    result1 = dxdt(x, t, kind="finite_difference", k=1)\n\n    # Savitzky-Golay using cubic polynomials to fit in a centered window of length 1\n    result2 = dxdt(x, t, kind="savitzky_golay", left=.5, right=.5, order=3)\n\n    # Spectral derivative\n    result3 = dxdt(x, t, kind="spectral")\n\n    # Spline derivative with smoothing set to 0.01\n    result4 = dxdt(x, t, kind="spline", s=1e-2)\n\n    # Total variational derivative with regularization set to 0.01\n    result5 = dxdt(x, t, kind="trend_filtered", order=1, alpha=1e-2)\n\nProject references:\n\n[1] Numerical differentiation of experimental data: local versus global methods- K. Ahnert and M. Abel  \n\n[2] Numerical Differentiation of Noisy, Nonsmooth Data- Rick Chartrand  \n\n[3] The Solution Path of the Generalized LASSO- R.J. Tibshirani and J. Taylor\n',
    'author': 'Andy Goldschmidt',
    'author_email': 'andygold@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andgoldschmidt/primelab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
