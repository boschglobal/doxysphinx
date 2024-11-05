doxysphinx
==========

.. py:module:: doxysphinx

.. autoapi-nested-parse::

   Doxysphinx main package.

   Doxysphinx uses `click <https://click.palletsprojects.com/>`_ to provide a command line interface with
   sub commands similar to e.g. ``git``.

   The main command is :func:`doxysphinx.cli.cli()`.
   The `build` and `clean` commands are defined in :mod:`doxysphinx.cli`.
   The commands itself will do some input validation and then call into the :class:`doxysphinx.process.Builder`
   which is considered the entrypoint of the main doxysphinx functionality.



Subpackages
-----------

.. toctree::
   :maxdepth: 1

   /docs/auto_api/doxysphinx/utils/index


Submodules
----------

.. toctree::
   :maxdepth: 1

   /docs/auto_api/doxysphinx/cli/index
   /docs/auto_api/doxysphinx/doxygen/index
   /docs/auto_api/doxysphinx/html_parser/index
   /docs/auto_api/doxysphinx/process/index
   /docs/auto_api/doxysphinx/resources/index
   /docs/auto_api/doxysphinx/sphinx/index
   /docs/auto_api/doxysphinx/toc/index
   /docs/auto_api/doxysphinx/writer/index


