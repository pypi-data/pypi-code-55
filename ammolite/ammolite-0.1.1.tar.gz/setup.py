# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biotite2pymol']

package_data = \
{'': ['*']}

install_requires = \
['biotite>=0.21,<0.22']

setup_kwargs = {
    'name': 'ammolite',
    'version': '0.1.1',
    'description': 'Visualize structure data from Biotite with PyMOL',
    'long_description': ".. image:: https://raw.githubusercontent.com/biotite-dev/biotite2pymol/master/doc/static/assets/biotite2pymol_logo_s.png\n  :alt: biotite2pymol logo\n  :align: center\n\nbiotite2pymol - From Biotite to PyMOL and back again\n====================================================\n\nThis package enables the transfer of structure related objects\nfrom `Biotite <https://www.biotite-python.org/>`_\nto `PyMOL <https://pymol.org/>`_ for visualization,\nvia PyMOL's Python API:\n\n- Import ``AtomArray`` and ``AtomArrayStack`` objects into *PyMOL* -\n  without intermediate structure files.\n- Convert *PyMOL* objects into ``AtomArray`` and ``AtomArrayStack`` instances.\n- Use *Biotite*'s boolean masks for atom selection in *PyMOL*.\n\nHave a look at the `example Jupyter notebook <https://github.com/biotite-dev/biotite2pymol/blob/master/doc/examples/cytochrome.ipynb>`_.\n\n|\n\n.. image:: https://raw.githubusercontent.com/biotite-dev/biotite2pymol/master/doc/demo/demo.gif\n    :alt: biotite2pymol demo\n\n|\n\n*PyMOL is a trademark of Schrodinger, LLC.*",
    'author': 'Patrick Kunzmann',
    'author_email': 'patrick.kunzm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ammolite.biotite-python.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
