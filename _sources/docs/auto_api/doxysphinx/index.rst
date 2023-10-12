:py:mod:`doxysphinx`
====================

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
   :titlesonly:
   :maxdepth: 3

   utils/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   cli/index.rst
   doxygen/index.rst
   html_parser/index.rst
   process/index.rst
   resources/index.rst
   sphinx/index.rst
   toc/index.rst
   writer/index.rst


