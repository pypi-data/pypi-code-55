# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.append(os.path.abspath("./_ext"))

# -- DocInit configuration ---------------------------------------------------

from docinit.docinit import get_config, set_vars
config = get_config()

# -- Project information -----------------------------------------------------

project = config['docinit']['name']
author = config['docinit']['author']
copyright = config['docinit']['copyright']
version = config['docinit']['version']
release = config['docinit']['release']
language = 'en'

# -- Setup--------------------------------------------------------------------

rst_prolog = """
.. |br| raw:: html

   <br>
.. |project| replace:: {0}
""".format(project)

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.intersphinx',
    'autoapi.extension',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'includefirst'
]

intersphinx_mapping = { 'python': ('https://docs.python.org/3', None) }
if config['docinit']['parent_url']:
    intersphinx_mapping['__parent__'] = (config['docinit']['parent_url'] + f'/{language}/latest', None)

templates_path = ['_templates']
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autoapi_dirs = config['docinit']['packages']
autoapi_type = 'python'
autoapi_root = 'api'
autoapi_python_class_content = 'both'
autoapi_python_use_implicit_namespaces = True
autoapi_add_toctree_entry = True
autoapi_options = ['members', 'undoc-members', 'show-inheritance']
autoapi_template_dir = '_templates/autoapi'

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_ivar = True

pygments_style = 'sphinx'

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'display_version': True
}
if config['docinit']['analytics']:
    html_theme_options['analytics_id'] = config['docinit']['analytics']
if config['docinit']['canonical_url']:
    html_theme_options['canonical_url'] = config['docinit']['canonical_url']
html_show_sourcelink = False
html_show_sphinx = False
html_logo = '_static/logo.png' if config['docinit']['logo_url'] else None
html_favicon = '_static/favicon.ico' if config['docinit']['favicon_url'] else None
html_static_path = ['_static']
html_css_files = ['docinit.css']
if config['docinit']['parent_url']: html_js_files = ['back.js']

# -- Overrides ---------------------------------------------------------------

set_vars(globals(), config)
