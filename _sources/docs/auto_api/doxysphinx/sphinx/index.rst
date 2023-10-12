:py:mod:`doxysphinx.sphinx`
===========================

.. py:module:: doxysphinx.sphinx

.. autoapi-nested-parse::

   The sphinx module contains classes that are tied to sphinx or resemble sphinx logic.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   doxysphinx.sphinx.DirectoryMapper
   doxysphinx.sphinx.SphinxHtmlBuilderDirectoryMapper




.. py:class:: DirectoryMapper(sphinx_source_dir: pathlib.Path, sphinx_output_dir: pathlib.Path)


   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.sphinx.DirectoryMapper
      :parts: 1

   Mapper that will calculate the output file path for an input file.

   In docs-as-code tooling (e.g. sphinx) often files from a source dir
   structure are processed and written to result files in a target dir structure.

   The make this mapping an implementation detail this protocol exists.
   It should be implemented for any special handling in mapping files.

   .. py:method:: map(path: pathlib.Path) -> pathlib.Path

      Calculate the path in output for a given path in input.



.. py:class:: SphinxHtmlBuilderDirectoryMapper(sphinx_source_dir: pathlib.Path, sphinx_output_dir: pathlib.Path)


   Mapper that will calculate the output file path for an input file.

   This is based on the logic that the sphinx html builder would use.

   .. py:method:: map(path: pathlib.Path) -> pathlib.Path

      Calculate the path in output for a given path in input.



