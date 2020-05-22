# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../.'))

# -- General information about the project --------------------------------
project = 'caeli'
copyright = '2020, Jackson Roehrig & Maria Paula Lorza Villegas'
author = 'Jackson Roehrig & Maria Paula Lorza Villegas'

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax']

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output ----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_options = {'navigation_depth': 4,}

html_static_path = ['_static']

autodoc_default_options = {
    'members':         True,
    'member-order':    'bysource',
}

