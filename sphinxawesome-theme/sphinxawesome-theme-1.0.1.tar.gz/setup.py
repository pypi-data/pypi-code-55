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
    'version': '1.0.1',
    'description': 'A simple theme for a Sphinx documentation',
    'long_description': '====================\nSphinx awesome theme\n====================\n   \n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue&style=for-the-badge\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n   :class: badge\n   \n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme?style=for-the-badge\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n   :class: badge\n\n.. image:: https://api.netlify.com/api/v1/badges/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22/deploy-status\n   :target: https://sphinxawesome.xyz\n   :alt: Netlify Status\n   :class: badge\n\nThis is a simple but awesome theme for the `Sphinx\n<http://www.sphinx-doc.org/en/master/>`_ documentation generator.\n\n\n------------\nInstallation\n------------\n\nInstall the theme as a Python package:\n\n.. code:: console\n\n   pip install sphinxawesome-theme\n\nTo use the theme, set ``html_theme`` in the Sphinx configuration file\n``conf.py``:\n\n.. code:: python\n\n   html_theme = "sphinxawesome_theme"\n\n-------------\nConfiguration\n-------------\n\nTo show also entries in the navigation menu from `toctree\n<https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html?highlight=toctree#directive-toctree>`_\ndirectives with the ``:hidden:`` option, add the following setting to the Sphinx\nconfiguration file ``conf.py``.\n\n.. code:: python\n\n   html_theme_options = {"nav_include_hidden": True}\n\nIncluding ``:hidden:`` in a toctree directive makes Sphinx include the documents, but\nnot print the list of links to the documents on the current page. This is useful when\nnavigation links are shown elsewhere, for example in a menu on the left side. The\ndefault is ``nav_include_hidden=False`` in order to be compatible with other themes.\n\n-----------\nLimitations\n-----------\n\nThis theme is designed to be simple. Some features are not (or not yet) available.\n\n- Zero custom theme variables to modify styles.\n- API documentation has not been tested. Some styles are missing. \n- Not all docutils/Sphinx roles have styles. There are a lot of them. \n- Internationalization was neglected.\n\n.. include-until-here\n\n-------------\nDocumentation\n-------------\n\nRead the documentation and see how the theme looks on the `demo page\n<https://sphinxawesome.xyz>`_\n',
    'author': 'Kai Welke',
    'author_email': '17420240+kai687@users.noreply.github.com',
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
