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

Doxysphinx uses click to provide a command line interface with sub commands.

The main command is :func:`doxysphinx.cli.cli()`.
The "build" and "clean" commands are defined in :mod:`doxysphinx.commands`.
The commands itself will do some input validation and then call into the
:class:`doxysphinx.builders.doxygen_rst_builder` which is considered the entry
point of the main doxysphinx functionality.
"""
