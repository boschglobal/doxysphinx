:py:mod:`doxysphinx.toc`
========================

.. py:module:: doxysphinx.toc

.. autoapi-nested-parse::

   The toc module contains classes related to the toctree generation for doxygen htmls/rsts.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   doxysphinx.toc.TocGenerator
   doxysphinx.toc.DoxygenTocGenerator




.. py:class:: TocGenerator(source_dir: pathlib.Path)


   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.toc.TocGenerator
      :parts: 1

   TocGenerator protocol.

   Gets the source_dir (with the html sources) during init and
   each file to possibly generate a toctree directive for in the :meth:`generate_toc_for`
   method. The implementer has then to choose how to implement the toc generation.

   .. py:method:: generate_toc_for(file: pathlib.Path) -> Iterable[str]

      Generate a toctree directive for a given file.

      :param file: the file to generate the toctree directive for
      :return: a string interable representing the lines forming the toctree directive



.. py:class:: DoxygenTocGenerator(source_dir: pathlib.Path)


   A TocGenerator for doxygen.

   Will read the menudata.js to check whether a toctree
   directive needs to be generated or not.

   .. py:method:: generate_toc_for(file: pathlib.Path) -> Iterator[str]

      Generate a toctree directive for a given file.

      Note that the toctree will only be generated when the file is part of a menu
      structure.
      :param file: the file to generate the toctree directive for
      :return: a string iterator representing the lines forming the toctree directive



