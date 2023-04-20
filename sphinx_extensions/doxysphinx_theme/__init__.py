# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Aniket Salve, Robert Bosch GmbH
# =====================================================================================

"""Doxysphinx themes extension.

This extensions add custom javascript files depending on theme.
Currently only supporting Book and RTD theme.
"""

import logging
import pathlib

from sphinx.application import Sphinx
from sphinx.config import Config


def setup(app: Sphinx):
    """Setups up the doxysphinx themes extension."""
    app.connect("config-inited", doxysphinx_theme_extension)
    return {"parallel_read_safe": True, "parallel_write_safe": True, "version": "0.1.0"}


def doxysphinx_theme_extension(app: Sphinx, config: Config):
    """Add custom javascript files specific to theme and set theme options.

    :param app: Sphinx app
    :param config: Sphinx config
    """
    current_file_path = pathlib.Path(__file__).parent.resolve()

    config.html_static_path.append(str(current_file_path) + "/_static/")

    if config.html_theme == "sphinx_book_theme":
        app.add_js_file("js/customize-navbar-book.js")
        app.add_css_file("css/sphinx-book-theme-custom.css")

    elif config.html_theme == "sphinx_rtd_theme":
        app.add_js_file("js/customize-navbar-rtd.js")
        app.add_css_file("css/sphinx-rtd-theme-custom.css")
        if config.html_theme_options["collapse_navigation"]:
            logging.warning("We are forcefully setting 'collapse_navigation' flag to 'False' in RTD theme options")
        config.html_theme_options["collapse_navigation"] = False
