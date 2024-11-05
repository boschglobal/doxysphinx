doxysphinx.writer
=================

.. py:module:: doxysphinx.writer

.. autoapi-nested-parse::

   The writer module contains classes that write the docs-as-code output files.



Classes
-------

.. autoapisummary::

   doxysphinx.writer.Writer
   doxysphinx.writer.RstWriter


Module Contents
---------------

.. py:class:: Writer(source_directory: pathlib.Path, toc_generator_type: Type[doxysphinx.toc.TocGenerator] = DoxygenTocGenerator)

   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.writer.Writer
      :parts: 1


   Protocol representing a Writer that write docs-as-code files.


   .. py:method:: write(parse_result: doxysphinx.html_parser.HtmlParseResult, target_file: pathlib.Path, html_hash: str) -> pathlib.Path

      Write a parsed html result to a target file.

      The format of that file is controlled by the concreate Writer implementation.

      :param parse_result: The result of a previous html parser run
      :param target_file: The target file to write
      :return: The written file (should be always identical to target_file input, but
          allows chaining...)



.. py:class:: RstWriter(source_directory: pathlib.Path, toc_generator_type: Type[doxysphinx.toc.TocGenerator] = DoxygenTocGenerator)

   Writes sphinx-rst files to disk.


   .. py:method:: write(parse_result: doxysphinx.html_parser.HtmlParseResult, target_file: pathlib.Path, html_hash: str) -> pathlib.Path

      Write html content to the target_file.

      :param parse_result: The result of the html parsing (=content + metadata)
      :param target_file:  The target docs-as-code (e.g. rst) file
      :return: The path the file was written to.



