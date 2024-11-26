# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
# Set the environment variable to indicate this is a documentation build. Needs to be a string. This causes run.py
# to not call create_app, which is instead called here.
os.environ["SPHINX_BUILD"] = '1'
# Add the project directory to sys.path
sys.path.insert(0, os.path.abspath('..'))

# Import the application. We are using the DocumentationConfig so that we can build the documentation outside of Docker.
from website import create_app
app = create_app('documentation')

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Docker-Flask-Template'
copyright = '2024, Zuicie'
author = 'Zuicie'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_static_path = ['_static']
