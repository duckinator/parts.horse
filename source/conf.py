# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import subprocess

project = 'Parts Horse'
copyright = '2023, Ellen Marie Dash'
author = 'Ellen Marie Dash'
release = subprocess.run(['git', 'rev-list', '--count', 'main'],
                         check=True, capture_output=True
                         ).stdout.decode().strip()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
]

# The master toctree document.
#master_doc = 'navbar'

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'sphinx_rtd_theme'
#html_theme = 'classic'
#html_static_path = ['_static']
