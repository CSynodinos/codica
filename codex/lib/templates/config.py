SPHINX_CONFIG_TEMPLATE = '''\
# Configuration file for the Sphinx documentation builder.
#
# This file contains a selection of the most common options.

import os
import sys
import types
sys.path.append(os.getcwd())

# -- Monkey-patch for Sphinx stringify_annotation bug -------------------------
# Sphinx can crash with "TypeError: 'NoneType' object cannot be interpreted
# as an integer" when autodoc encounters objects with a broken __len__/__bool__.
import sphinx.util.typing as _sphinx_typing
_orig_stringify = _sphinx_typing.stringify_annotation
def _safe_stringify(annotation, mode='fully-qualified', short_literals=False):
    try:
        return _orig_stringify(annotation, mode=mode, short_literals=short_literals)
    except TypeError:
        return repr(annotation)
_sphinx_typing.stringify_annotation = _safe_stringify

# -- Project information -----------------------------------------------------
project = 'My Project'
author = 'Author Name'
release = '0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.apidoc',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinxemoji.sphinxemoji',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

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