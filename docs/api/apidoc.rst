..
  =====================================================================================
   C O P Y R I G H T
  -------------------------------------------------------------------------------------
  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

  Author(s):
  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
  =====================================================================================

=================================
API Reference
=================================
.. currentmodule:: doxysphinx

This is the api reference for doxysphinx.

.. rubric:: doxysphinx package

Doxysphinx uses `click <https://click.palletsprojects.com/>`_ to provide a command line interface with sub
commands similar to e.g. ``git``.

The main command is :func:`doxysphinx.cli.cli()`.
The "build" and "clean" commands are defined in :mod:`doxysphinx.commands`.
The commands itself will do some input validation and then call into the
:class:`doxysphinx.builders.doxygen_rst_builder` which is considered the entry
point of the main doxysphinx functionality.

.. autosummary::
   :toctree: doxysphinx
   :recursive:

   cli
   doxygen
   html_parser
   process
   resources
   sphinx
   writer

.. currentmodule:: doxysphinx.utils

.. rubric:: doxysphinx.utils modules

Utils package with several helpers not related to main application logic.

.. autosummary::
   :toctree: doxysphinx.utils
   :recursive:

   contexts
   exceptions
   files
   iterators
   .pathlib_fix
