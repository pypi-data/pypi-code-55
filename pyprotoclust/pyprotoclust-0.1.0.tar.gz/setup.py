# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyprotoclust']

package_data = \
{'': ['*'], 'pyprotoclust': ['cpp/include/*', 'cpp/src/*']}

install_requires = \
['tqdm>=4.46.0,<5.0.0']

extras_require = \
{'cython': ['cython>=0.29.17,<0.30.0'],
 'docs': ['sphinx>=3.0.3,<4.0.0',
          'sklearn>=0.0,<0.1',
          'scipy>=1.4.1,<2.0.0',
          'nbsphinx>=0.7.0,<0.8.0',
          'jupyter_client>=6.1.3,<7.0.0',
          'ipykernel>=5.2.1,<6.0.0',
          'matplotlib>=3.2.1,<4.0.0',
          'ipywidgets>=7.5.1,<8.0.0']}

setup_kwargs = {
    'name': 'pyprotoclust',
    'version': '0.1.0',
    'description': 'Hierarchical clustering using minimax linkage.',
    'long_description': ".. image:: https://readthedocs.org/projects/pyprotoclust/badge/?version=latest\n   :target: https://pyprotoclust.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n   :target: https://lbesson.mit-license.org/\n   :alt: MIT License\n\n**Pyprotoclust** is an implementatin of representative hierarchical clustering using minimax linkage.\n\nThe original algorithm is from\n`Hierarchical Clustering With Prototypes via Minimax Linkage <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4527350/>`_\nby Jacob Bien and Robert Tibshirani.\n\nPyprotoclust takes a distance matrix as input. It returns a linkage matrix encoding the hierachical clustering as well\nas an additional list labelling the prototypes associated with each clustering. This allows a user to integrate with\nthe existing tools in the\n`SciPy hierarchical clustering module <https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html>`_.\n\nInstallation:\n\n.. code-block:: python\n\n    pip install pyprotoclust\n\nUsage:\n\n.. code-block:: python\n\n    from pyprotoclust import protoclust\n    import numpy as np\n    import scipy as sp\n    import scipy.cluster.hierarchy\n    import scipy.spatial.distance\n\n    # Generate two-dimensional toy data\n    n = 60\n    np.random.seed(4)\n    params = [{'mean': [-7, 0], 'cov': [[1, 1], [1, 5]]},\n              {'mean': [1, -1], 'cov': [[5, 0], [0, 1]]},\n              {'mean': [3, 7], 'cov': [[1, 0], [0, 1]]}]\n    data = np.vstack([np.random.multivariate_normal(p['mean'], p['cov'], n) for p in params])\n    X = sp.spatial.distance.squareform(sp.spatial.distance.pdist(data))\n\n    # Produce a hierarchical clustering using minimax linkage\n    Z, prototypes = protoclust(X)\n\n    # Generate clusters at a set cut_height using scipy's hierarchy module\n    cut_height = 7\n    T = sp.cluster.hierarchy.fcluster(Z, cut_height, criterion='distance')\n    L,M = sp.cluster.hierarchy.leaders(Z, T)\n\n    # Get the prototypes associated with the generated clusters\n    P = data[prototypes[L]]\n\n\nThe previous example produces a linkage matrix Z and prototypes P that can be used to produce dendrograms and other\nplots of the data.\n\n.. figure:: docs/images/dendrogram.png\n    :width: 400\n    :align: center\n    :alt: A dendrogram of the hierarchical clustering example.\n\n    *A dendrogram of the hierarchical clustering example with a dashed line at the example cut height.*\n\n.. figure:: docs/images/scatter.png\n    :width: 400\n    :align: center\n    :alt: A scatter plot of the  hierarchical clustering example.\n\n    *A scatter plot of the example with circles centered at prototypes drawn with radii equal to the top-level\n    linkage heights of each cluster.*",
    'author': 'Andy Goldschmidt',
    'author_email': 'andygold@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andgoldschmidt/pyprotoclust',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
