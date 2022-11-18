# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

"""
Doxysphinx main package.

Doxysphinx uses `click <https://click.palletsprojects.com/>`_ to provide a command line interface with
sub commands similar to e.g. ``git``.

The main command is :func:`doxysphinx.cli.cli()`.
The `build` and `clean` commands are defined in :mod:`doxysphinx.cli`.
The commands itself will do some input validation and then call into the :class:`doxysphinx.process.Builder`
which is considered the entrypoint of the main doxysphinx functionality.
"""
