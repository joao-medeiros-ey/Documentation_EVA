# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath("../api")) # assume que o diretório anterior é o pai da pasta docs


project = 'EVA Flask 1.0'
copyright = '2025, Luis Fernando; Clara Selistre; Luane Testa; Jaqueline Amorim; João Medeiros'
author = 'Luis Fernando; Clara Selistre; Luane Testa; Jaqueline Amorim; João Medeiros'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',          # para docstrings via autodoc
    'sphinx.ext.napoleon',         # para suporte a Google/Numpy style
    'sphinx_autodoc_typehints',    # para exibir anotações de tipos
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en_US'

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": False,
    "special-members": False,
    "exclude-members": "os,environ,OPENAI_API_KEY,OPENAI_API_ENDPOINT,OPENAI_API_VERSION,DIRECTORY_PATH,OPENAI_MODEL_NAME,TESTE,MODEL_PATH,OPENAI_API_KEY_EMBEDDING_MODEL,OPENAI_API_VERSION_EMBEDDING_MODEL,OPENAI_API_ENDPOINT_EMBEDDING_MODEL,OPENAI_EMBEDDING_MODEL,BLOB_CONNECTION_STRING,BLOB_CONTAINER_NAME,BLOB_INDEX_BLOB,BLOB_METADATA_BLOB"
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
