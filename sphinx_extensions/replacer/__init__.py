# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

"""Sphinx replacer extension.

This module represents a sphinx extension that processes sphinx input files with jinja before building
the doctree.
"""

from sphinx.application import Sphinx

# This extension is based on the excellent findings of Adam Szymd (aszmyd):
# https://github.com/sphinx-doc/sphinx/issues/4054#issuecomment-329097229
# and Eric Holscher:
# https://ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/


def setup(app: Sphinx):
    """Setups up the replacer extension."""
    app.connect("source-read", JinjaReplacer.source_read_handler)

    return {"parallel_read_safe": True, "parallel_write_safe": True, "version": "0.1.0"}


class JinjaReplacer:
    """Replaces occurences of jinja expressions."""

    @staticmethod
    def source_read_handler(app, docname, source):
        """Sphinx event handler for the "source-read" event.

        :param app: sphinx application
        :param docname: the name of the document
        :param source: the content of the document
        """
        if app.builder.format != "html":
            return
        source_text = source[0]
        rendered = app.builder.templates.render_string(source_text, app.config.html_context)
        source[0] = rendered
