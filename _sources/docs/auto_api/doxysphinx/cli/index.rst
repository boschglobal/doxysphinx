doxysphinx.cli
==============

.. py:module:: doxysphinx.cli

.. autoapi-nested-parse::

   Entry module for the doxysphinx cli.

   Defines click main command (:func:`cli`) and subcommands (:func:`build`), (:func:`clean`)

   .. note::

       * Execute this script directly to start doxysphinx.

       * If you need to call a function to start doxysphinx (e.g. for vscode launch config etc.) use the
         :func:`cli` directly.

           Sphinx autodoc which created this documentation seems to have problems with decorated methods.
           The function signatures shown here in the documentation aren't correct. Just click on view source to
           see the correct signatures.



Classes
-------

.. autoapisummary::

   doxysphinx.cli.DoxygenContext


Functions
---------

.. autoapisummary::

   doxysphinx.cli.cli
   doxysphinx.cli.build
   doxysphinx.cli.clean


Module Contents
---------------

.. py:class:: DoxygenContext

   Represent the options for doxygen that can be set via the cli.

   The doxygen projects are specified through INPUT (multiple possible). INPUT can be:

   * a doxygen configuration file (aka doxyfile)

   * a directory, which contains the generated doxygen html documentation.
     Note that specifying a directory will skip the config validation completely and is therefore considered
     "advanced stuff". You will typically want to use that if you're integrating doxysphinx in a ci build
     system. If unsure, use a doxyfile.


   .. py:attribute:: input
      :type:  List[pathlib.Path]


   .. py:attribute:: doxygen_exe
      :type:  str


   .. py:attribute:: doxygen_cwd
      :type:  pathlib.Path


.. py:function:: cli()

   Integrates doxygen html documentation with sphinx.

   Doxysphinx typically should run right after doxygen. It will generate rst files out of doxygen's html
   files. This has the implication, that the doxygen html output directory (where the rst files are generated
   to) has to live inside sphinx's input tree.


.. py:function:: build(parallel: bool, sphinx_source: pathlib.Path, sphinx_output: pathlib.Path, **kwargs)

   Build rst and copy related files for doxygen projects.

   SPHINX_SOURCE specifies the root of the sphinx source directory tree while SPHINX_OUTPUT specifies the root of the
   sphinx output directory tree.



   .. warning::

      * when using ``sphinx-build -b html SOURCE_DIR OUTPUT_DIR ...`` the html output will be put to ``OUTPUT_DIR`` so
        so doxysphinx's ``SPHINX_OUTPUT`` should be ``OUTPUT_DIR``.
      * when using ``sphinx-build -M html`` the html output will be put to ``OUTPUT_DIR/html`` so doxysphinx's
        ``SPHINX_OUTPUT`` should be ``OUTPUT_DIR/html``.


.. py:function:: clean(parallel: bool, sphinx_source: pathlib.Path, sphinx_output: pathlib.Path, **kwargs)

   Clean up files created by doxysphinx.

   SPHINX_SOURCE specifies the root of the sphinx source directory tree while SPHINX_OUTPUT specifies the root of the
   sphinx output directory tree. The doxygen html outputs are specified through INPUT (multiple possible) either
   by pointing to the doxygen html output directory or by pointing to the doxygen config file (doxyfile).


