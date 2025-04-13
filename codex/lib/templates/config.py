SPHINX_CONFIG_TEMPLATE = '''\
# Configuration file for the Sphinx documentation builder.
#
# This file contains a selection of the most common options.

import os
import sys
sys.path.append(os.getcwd())

# -- Project information -----------------------------------------------------
project = 'My Project'
author = 'Author Name'
release = '0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.apidoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinxemoji.sphinxemoji',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# The master document.
master_doc = 'index'

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

# Do not prepend module names to objects (for cleaner output)
add_module_names = False
html_theme_options = {
    "back_to_top_button": True,
    # Toc options
    'collapse_navigation': False,
    "show_nav_level": 2,
    "show_toc_level": 6,
}
'''