# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))
# print(os.getcwd())


# -- Project information -----------------------------------------------------

project = 'Moildev 4.0'
copyright = '2022, moil-lab'
author = 'moil-lab'

# The full version, including alpha/beta/rc tags
release = '2022'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.viewcode",
              "sphinx.ext.napoleon",
              "sphinx.ext.autosectionlabel"
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

master_doc = 'index'

autoclass_content = 'both'
# autodoc_mock_imports = ["Moildev", "PyQt6", "PyQt5", "cv2", "numpy", "pyexiv2"]
html_show_sourcelink = False

autodoc_default_flags = ['members', 'inherited-members']
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'undoc-members': True,
    'show-inheritance': True}

autosummary_generate = True

add_module_names = False

# html_context = {
#     "display_github": True, # Integrate GitHub
#     "github_user": "MoilOrg", # Username
#     "github_repo": "release_moildev_4_0", # Repo name
#     "github_version": "main", # Version
#     "conf_py_path": "docs/source/", # Path in the checkout to the docs root
# }


