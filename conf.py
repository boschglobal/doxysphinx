# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""sphinx configuration file."""

# pylint: disable=invalid-name

import os
import sys

sys.path.append(os.path.abspath("."))

from conf_utils import (  # noqa E402, pylint: disable=wrong-import-position
    last_updated_from_git,
    multi_glob,
    theme_options,
    version_from_project_toml,
)

# General information about the project.
project = "Doxysphinx"
html_show_copyright = False

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# version = informational_version_from_ci('0.1.0-local-development-version')
# release = semantic_version_from_ci('0.1')
version = version_from_project_toml()
release = version_from_project_toml()

# -- General configuration ---------------------------------------------------
needs_sphinx = "4.4.0"
source_suffix = ".rst"
master_doc = "index"
language = "en"
templates_path = ["docs/_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = multi_glob(
    ".*",
    "_*",
    "dist",
    "demo",
    "docs/_templates",
    "docs/auto_api/index.rst",
    "NOTICE.md",
    "LICENSE.md",
    "CHANGELOG.md",
    "README.md",
    "external/README.md",
    "tests",
)

# -- Options for HTML output -------------------------------------------------
# Configure HTML theme (remember to also change doxysphinx)
# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_book_theme"
html_theme_options = theme_options(html_theme)
html_static_path = ["docs/_static/"]
html_title = project
html_css_files = [f"{html_theme.replace('_', '-')}-custom.css"]
html_logo = "docs/resources/doxysphinx_logo.svg"
html_last_updated_fmt = last_updated_from_git(html_theme_options["repository_url"])

github_username = "anyone"  # these just need to be set that the sphinx toolbox extension will work
github_repository = "any"
# -- Sphinx extensions -------------------------------------------------------
extensions = [
    "sphinxcontrib.needs",
    "sphinxcontrib.plantuml",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "sphinx.ext.viewcode",
    "myst_parser",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.duration",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinxcontrib.doxylink",
    "sphinx.ext.inheritance_diagram",
    "sphinx_design",
    # in-repo sphinx extensions:
    "sphinx_extensions.replacer",
]

# Plantuml
plantuml = "java -Djava.awt.headless=true -jar /usr/share/plantuml/plantuml.jar"
plantuml_output_format = "svg"

# Autoapi
autoapi_dirs = ["doxysphinx"]
autoapi_root = "docs/auto_api"
autoapi_options = ["members", "undoc-members", "show-inheritance", "show-inheritance-diagram", "show-module-summary"]
autoapi_keep_files = True
autoapi_add_toctree_entry = False
autodoc_typehints = "signature"

# Myst
myst_enable_extensions = ["colon_fence"]
myst_heading_anchors = 4

# replacer substitutions (can also be given via sphinx -A cli options)
gh_repo = "https://github.com/boschglobal/doxysphinx"
html_context = {
    "repo": f"{gh_repo}",
    "code": f"{gh_repo}/tree/main",
}

# needs
# types definition for sphinx needs
needs_types = [
    {
        "directive": "component",
        "title": "Software Component",
        "prefix": "COMP_",
        "color": "#99E8FF",
        "style": "component",
    },
    {
        "directive": "feature",
        "title": "Software Feature",
        "prefix": "FEAT_",
        "color": "#58DD63",
        "style": "folder",
    },
    {
        "directive": "req",
        "title": "Software Requirement",
        "prefix": "REQ_",
        "color": "#37CCB8",
        "style": "folder",
    },
    {
        "directive": "test",
        "title": "Software Test",
        "prefix": "TEST_",
        "color": "#DDA01A",
        "style": "folder",
    },
]

needs_extra_options = ["category", "provider"]

needs_extra_links = [
    {"option": "requires", "incoming": "is required by", "outgoing": "requires"},
    {
        "option": "derives",
        "incoming": "is derived to",
        "outgoing": "is derived from",
    },
    {
        "option": "implements",
        "incoming": "is implemented by",
        "outgoing": "implements",
    },
    {"option": "tracks", "incoming": "tracks", "outgoing": "is tracked by"},
]

# Doxylink (note that the second parameter of the tuple indicates a path relative to
# the sphinx output home)
doxygen_root = "docs/doxygen"
doxylink = {
    "demo": (
        f"{doxygen_root}/demo/html/tagfile.xml",
        f"{doxygen_root}/demo/html",
    ),
}
