# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['sphinx>3']

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '1.3.0',
    'description': 'A simple theme for a Sphinx documentation',
    'long_description': '====================\nSphinx awesome theme\n====================\n   \n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue&style=for-the-badge\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n   :class: badge\n   \n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme?style=for-the-badge\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n   :class: badge\n\n.. image:: https://img.shields.io/netlify/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22?style=for-the-badge\n   :target: https://sphinxawesome.xyz\n   :alt: Netlify Status\n   :class: badge\n\nThis is a simple but awesome theme for the `Sphinx\n<http://www.sphinx-doc.org/en/master/>`_ documentation generator.\n\n\n------------\nInstallation\n------------\n\n.. install-start\n\nInstall the theme as a Python package:\n\n.. code:: console\n\n   pip install sphinxawesome-theme\n\n.. install-end\n\n-----\nUsage\n-----\n\n.. use-start\n\nTo use the theme, set ``html_theme`` in the Sphinx configuration file\n``conf.py``:\n\n.. code:: python\n\n   html_theme = "sphinxawesome_theme"\n\nTo include all entries in the navigation menu, add the following setting to the Sphinx\nconfiguration file ``conf.py``.\n\n.. code:: python\n\n   html_theme_options = {"nav_include_hidden": True}\n\nIf you set the option ``:hidden:`` to a toctree_ directive, the content will be\nincluded, but the list of links to the documents will not be written on the page itself.\nThis can be useful when navigation links are shown elsewhere.\n\n.. _toctree: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree\n\nThe Sphinx awesome theme shows a navigation menu on the left side of all pages, so\nhaving the links shown in the content area is not necessary. In order allow an easy\ntransition from other Sphinx themes, the default is ``nav_include_hidden = False``.\n\nTo make best use of this theme, include the ``:hidden:`` option to all ``..toctree``\ndirectives and set ``nav_include_hidden = True``.\n\n.. use-end\n\n----\nDemo\n----\n\nSee how the theme looks on the `demo page <https://sphinxawesome.xyz>`_.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
